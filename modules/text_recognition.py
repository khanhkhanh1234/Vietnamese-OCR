import sys
if "../" not in sys.path:
    sys.path.append("../")
from modules.Base import Base
from config import production_config as cfg2
from vietocr.tool.config import Cfg
from vietocr.tool.predictor import Predictor

class TextRecognition(Base):
    def __init__(self, device="cpu"):
        
        self.config_path = cfg2.text_recognition_config_yml_path
        self.weights_path = cfg2.text_recognition_weights_path

        config = Cfg.load_config_from_file(self.config_path)
        config['device'] = device
        config['weights'] = self.weights_path
        self.recognizer = Predictor(config)

    def __call__(self, img):
        text, confidence = self.recognizer.predict(img, return_prob=True)
        return text, confidence
        

    