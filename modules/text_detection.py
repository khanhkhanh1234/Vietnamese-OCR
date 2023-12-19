import sys
if "../" not in sys.path:
    sys.path.append("../")

from modules.Base import Base
from paddleocr import PaddleOCR
import paddle
import numpy as np
import cv2

class TextDetection(Base):
    def __init__(self, device="cpu"):
        paddle.set_device(device)
        self.detector = PaddleOCR(lang='en', det=True, rec=False, cls=False, use_angle_cls=False)

    def __call__(self, image: np.ndarray, line_group=True):
        # Detection
        result = self.detector.ocr(image,rec=False)
        # Line link
        bboxes = np.array(result[0], dtype=int)
        if line_group:
            lines_bbox = self.line_group(bboxes)
        else:
            lines_bbox = [[bbox] for bbox in bboxes]
        # sort line top to bottom
        lines_bbox = TextDetection.sort_lines_bbox(lines_bbox)
        print("in line box _____")
        print(lines_bbox)
        # bbox to image
        lines_bboxes_image = []
        for line_bbox in lines_bbox:
            line_bbox_image = []
            for bbox in line_bbox:
                line_bbox_image.append((bbox, self.crop_image(image, bbox)))
            lines_bboxes_image.append(line_bbox_image)
        return lines_bboxes_image

    @staticmethod
    def create_line_equation(x1, y1, x2, y2):
        return lambda x, y: (y1-y2)*(x-x1)+(x2-x1)*(y-y1)

    @staticmethod
    def is_same_line(bbox1, bbox2):
        center_bbox2 = bbox2.mean(axis=0).astype(int)
        equation_top_bbox1 = TextDetection.create_line_equation(*bbox1[0], *bbox1[1])
        equation_bottom_bbox1 = TextDetection.create_line_equation(*bbox1[3], *bbox1[2])
        check = equation_top_bbox1(*center_bbox2) * equation_bottom_bbox1(*center_bbox2)
        return np.any(check < 0)

    @staticmethod
    def line_group(bboxes):
        n = len(bboxes)
        is_check = {i: False for i in range(n)}
        lines = []
        for i in range(0, n):
            if is_check[i]: continue
            line = []
            line.append(bboxes[i])
            is_check[i] = True
            if i < n-1:
                for j in range(i+1, n):
                    if is_check[j]: continue
                    if TextDetection.is_same_line(bboxes[i], bboxes[j]):
                        # print(f"Link {i} -> {j}")
                        line.append(bboxes[j])
                        is_check[j] = True
            line = sorted(line, key=lambda x: x[0][0])
            lines.append(line)
        return lines

    @staticmethod
    def sort_lines_bbox(lines_bbox):
        return sorted(lines_bbox, key=lambda x: x[0][0][1])

    @staticmethod
    def crop_image(img, poly):
        height = img.shape[0]
        width = img.shape[1]

        points1 = np.array(poly, dtype=np.float32)
        minx, miny, maxx, maxy = np.min(points1[:, 0]), np.min(points1[:, 1]), np.max(points1[:, 0]), np.max(points1[:, 1])
        points2 = np.array([
            [0, 0],
            [maxx - minx, 0],
            [maxx-minx, maxy-miny],
            [0, maxy-miny],
        ], dtype=np.float32)
        matrix = cv2.getPerspectiveTransform(points1, points2)
        result = cv2.warpPerspective(img, matrix, (int(maxx-minx), int(maxy-miny)))
        return result