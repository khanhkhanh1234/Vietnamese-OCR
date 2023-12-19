from modules.full_pipeline import FullPipeline
import cv2
import json

if __name__ == "__main__":
    pipeline = FullPipeline()
    front_image = cv2.imread(r"samples/front.png")
    inner_left_image = cv2.imread(r"samples/inner_left.jpg")
    inner_right_image = cv2.imread(r"samples/inner_right.jpg")
    back_image = cv2.imread(r"samples/back.jpg")
    data = pipeline(front_image, inner_left_image, inner_right_image, back_image)
    print(json.dumps(data, indent=4, ensure_ascii=False))