from modules.eval_ocr import EvalVietOCR    
import sys
import cv2

if __name__ == "__main__":
    # print(sys.argv[1])
    ocr_eval = EvalVietOCR(datatest_path=sys.argv[1])
    ocr_eval()