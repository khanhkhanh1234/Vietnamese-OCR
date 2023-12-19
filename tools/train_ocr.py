from modules.train_ocr import TrainVietOCR    
import sys
import cv2

if __name__ == "__main__":
    ocr_trainer = TrainVietOCR(dataset_path=sys.argv[1])
    ocr_trainer()