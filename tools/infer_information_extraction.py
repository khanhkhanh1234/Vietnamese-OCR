from modules.information_extraction import InformationExtraction

FRONT_PATH = r"samples/text_front.txt"
INNER_LEFT_PATH = r"samples/text_inner_left.txt"

if __name__ == "__main__":
    extractor = InformationExtraction()
    
    with open(FRONT_PATH, encoding="utf-8") as f:
        front = f.read()
        
    with open(INNER_LEFT_PATH, encoding="utf-8") as f:
        inner_left = f.read()
        
    extractor(front=front, inner_left=inner_left, is_debug=True)