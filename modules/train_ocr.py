import sys
import os
import warnings
warnings.filterwarnings('ignore')

if "../" not in sys.path:
    sys.path.append("../")

from modules.Base import Base
import numpy as np
import cv2
from config import params, dataset_params, config_yml_path, checkpoint_path
from vietocr.tool.config import Cfg
from vietocr.model.trainer import Trainer 


class TrainVietOCR(Base):
    def __init__(self, dataset_path, device="cpu", model='vgg_transformer'):
        global params, dataset_params, checkpoint_path

        if checkpoint_path is None:
            checkpoint_path = os.path.join(os.path.expanduser("~"), ".cache", "pbl6", "checkpoint", "transformerocr_checkpoint.pth")
            os.makedirs(os.path.join(os.path.expanduser("~"), ".cache", "pbl6", "checkpoint"), exist_ok=True)

        params['check_point'] = checkpoint_path
        dataset_params['data_root'] = dataset_path
        
        self.model = model
        self.config = Cfg.load_config_from_name(self.model)
        self.config['trainer'].update(params)
        self.config['dataset'].update(dataset_params)
        self.config['device'] = device
        self.trainer = Trainer(self.config, pretrained=False)

    def __call__(self):
        global config_yml_path
        if config_yml_path is None:
            config_yml_path = os.path.join(os.path.expanduser("~"), ".cache", "pbl6", "config.yml")
            os.makedirs(os.path.join(os.path.expanduser("~"), ".cache", "pbl6"), exist_ok=True)
        self.trainer.train()
        self.trainer.config.save(config_yml_path)
        print(self.trainer.precision())

    