from modules.text_detection import TextDetection    
from modules.text_recognition import TextRecognition
from modules.information_extraction import InformationExtraction
from PIL import Image 
import cv2
import numpy as np
from tqdm import tqdm
import base64

class FullPipeline:    
    def __init__(self, detector_device="cpu", reconition_device="cpu"):
        self.detector = TextDetection(device=detector_device)
        self.recognizer = TextRecognition(device=reconition_device)
        self.extractor = InformationExtraction()
    
    def __call__(self, front_image, inner_left_image, inner_right_image, back_image):
        front_text, inner_left_text, inner_right_text = "", "", ""
        land_image = None
        
        front_image = front_image[:, :, ::-1]
        inner_left_image = inner_left_image[:, :, ::-1] 
        inner_right_image = inner_right_image[:, :, ::-1]
        back_image = back_image[:, :, ::-1]

        if front_image is not None:
            print(">> Process on front")
            for line in tqdm(self.detector(front_image, False)):
                line_text = ""
                for bbox, image in line:
                    text, confidence = self.recognizer(Image.fromarray(image))
                    line_text = line_text + text
                print(">>", line_text)
                front_text = front_text + line_text + "\n"
                
        if inner_left_image is not None:
            print(">> Process on inner left")
            for line in tqdm(self.detector(inner_left_image,False)):
                line_text = ""
                for bbox, image in line:
                    text, confidence = self.recognizer(Image.fromarray(image))
                    line_text = line_text + text
                print(">>", line_text)
                inner_left_text = inner_left_text + line_text + "\n"   
                
        if inner_right_image is not None:
            print(">> Process on inner right")
            y1_graph, y2_graph = 0, -1
            x_col1 = None
            x_col2 = None
            for line in tqdm(self.detector(inner_right_image, False)):
                bbox, image = line[0]
                line_text, confidence = self.recognizer(Image.fromarray(image))
                # Find some fix location
                if line_text.startswith("III."):
                    y1_graph = max(bbox[:, 1])
                elif line_text.startswith("IV."):
                    y2_graph = min(bbox[:, 1])
                elif line_text.startswith("Nội dung"):
                    x_col1 = np.mean(bbox[:, 0])
                elif line_text.startswith("Xác nhận") or line_text.startswith("có thẩm quyền"):
                    x_col2 = np.mean(bbox[:, 0])
                # Add text
                elif x_col1 is not None and x_col2 is not None:
                    y = np.mean(bbox[:, 0])
                    if abs(y - x_col1) < abs(y - x_col2):
                        inner_right_text = inner_right_text + line_text + "\n"
            land_image = inner_right_image[y1_graph:y2_graph,:,:]
            
        if back_image is not None:
            print(">> Process on back in 12345")
            x_col1 = None
            x_col2 = None
            for line in tqdm(self.detector(back_image, False)):
                bbox, image = line[0]
                line_text, confidence = self.recognizer(Image.fromarray(image))
                # Find some fix location
                if line_text.startswith("Người được cấp Giấy chứng nhận"):
                    break
                elif line_text.startswith("Nội dung"):
                    x_col1 = np.mean(bbox[:, 0])
                elif line_text.startswith("Xác nhận") or line_text.startswith("có thẩm quyền"):
                    x_col2 = np.mean(bbox[:, 0])
                # Add text
                elif x_col1 is not None and x_col2 is not None:
                    y = np.mean(bbox[:, 0])
                    if abs(y - x_col1) < abs(y - x_col2):
                        inner_right_text = inner_right_text + line_text + "\n"
            
        data = self.extractor(front=front_text, inner_left=inner_left_text, is_debug=False)
        data["Những thay đổi sau khi cấp giấy chứng nhận"] = {"Nội dung thay đổi": inner_right_text}
        if land_image is not None:
            _, buffer = cv2.imencode('.jpg', land_image)
            jpg_as_text = base64.b64encode(buffer)
            data["land_image"] = jpg_as_text
        return data