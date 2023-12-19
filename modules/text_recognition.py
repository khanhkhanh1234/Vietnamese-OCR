import sys
if "../" not in sys.path:
    sys.path.append("../")
from modules.Base import Base
from config import text_recognition_config_yml_path, text_recognition_weights_path
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor
import gdown
import os

class TextRecognition(Base):
    def __init__(self, model_name='vgg_transformer', config_path='D:\Download\config (3) (2).yml', device="cpu", get_config_yml=False):
        global text_recognition_config_yml_path, text_recognition_weights_path
        if text_recognition_weights_path is None:
            text_recognition_weights_path = os.path.join(os.path.expanduser("~"), ".cache", "pbl6", "transformerocr.pth")
            os.makedirs(os.path.join(os.path.expanduser("~"), ".cache", "pbl6"), exist_ok=True)
            
        # if text_recognition_config_yml_path is None:
        #     text_recognition_config_yml_path = os.path.join(os.path.expanduser("~"), ".cache", "pbl6", "config.yml")
        #     os.makedirs(os.path.join(os.path.expanduser("~"), ".cache", "pbl6"), exist_ok=True)
            
        if not os.path.exists(text_recognition_weights_path):
            self.get_weights_from_gdrive(save_to=text_recognition_weights_path)
            
        # if os.path.exists(text_recognition_config_yml_path) and get_config_yml == True:
        #     self.get_config_yml_from_gdrive()
        #     config = Cfg.load_config_from_file(text_recognition_config_yml_path)
        else:
            config = Cfg.load_config_from_name(model_name)
        config = Cfg.load_config_from_file(config_path)
        config['device'] = device
        config['weights'] = text_recognition_weights_path
        self.recognizer = Predictor(config)

    # def get_config_yml_from_gdrive(self, save_to, url='https://drive.google.com/uc?id=156WvR35nXeAIzYWLi1Rw1xQWu0uSMKXp'):
    def get_config_yml_from_gdrive(self, save_to, url='https://drive.google.com/uc?export=download&id=1L1WtMtUeiaW7qEF4j8dYkeZpkRsH5Pjp'):
        gdown.download(url, save_to, quiet=False)
        print("Downloaded config.yml from gdrive")

    def get_weights_from_gdrive(self, save_to, url='https://drive.google.com/uc?export=download&id=1StVSthypXqUfEWSKC_K4eDWeisvjA-gu'):
        gdown.download(url, save_to, quiet=False)

    def __call__(self, img):
        text, confidence = self.recognizer.predict(img, return_prob=True)
        return text, confidence
        

    