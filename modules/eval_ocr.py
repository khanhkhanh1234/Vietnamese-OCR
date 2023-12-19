import sys
if "../" not in sys.path:
    sys.path.append("../")
from modules.Base import Base
from modules.text_recognition import TextRecognition
import cv2
import pandas as pd
from PIL import Image
import os

class EvalVietOCR(Base):
    def __init__(self, datatest_path, model_name='vgg_transformer', device="cpu", get_config_yml=False):
        self.text_recognizer = TextRecognition(model_name, device, get_config_yml)
        self.datatest_path = datatest_path

    def __call__(self):
        recs = []
        with open(os.path.join(self.datatest_path, 'test_annotation.txt')) as file_txt:
            lines = file_txt.readlines()
            for line in lines:
                image_path = os.path.join(self.datatest_path, line.split('\t')[0])
                image = cv2.imread(image_path)
                image = image[:, :, ::-1]
                text_pred, confidence = self.text_recognizer(Image.fromarray(image))
                ground_truth = line.split('\t')[-1]
                recs.append({
                    'ground_truth': ground_truth.strip(),
                    'predict': text_pred.strip(),
                    'confidence': confidence
                })
                print(f"Label: {ground_truth.strip()} Predict: {text_pred.strip()} --- {confidence}")
        df = pd.DataFrame(recs)
        df.to_csv('eval_result.csv', index=False)
        return df
        



    