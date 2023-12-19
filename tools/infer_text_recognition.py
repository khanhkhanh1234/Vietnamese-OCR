from modules.text_detection import TextDetection
from modules.text_recognition import TextRecognition
from PIL import Image
import cv2

IMG_PATH = r"samples/hm4.jpg"

def perform_text_detection_and_recognition(image_path):
    # Text Detection
    detector = TextDetection(device="cpu")
    image_detection = cv2.imread(image_path)
    clone_image_detection = image_detection.copy()
    image_detection = image_detection[:, :, ::-1]
    clone_image_detection = image_detection.copy()

    bounding_boxes_data = []  # List to store information for each bounding box

    for i, line in enumerate(detector(image_detection)):
        for bbox, image in line:
            clone_image_detection = cv2.polylines(clone_image_detection, [bbox], isClosed=True, color=(255, 0, 0),
                                                  thickness=1)

            # Crop the bounding box region
            x, y, w, h = cv2.boundingRect(bbox)
            cropped_image = image_detection[y:y + h, x:x + w]

            # Text Recognition
            recognizer = TextRecognition(device="cpu")
            text, confidence = recognizer(Image.fromarray(cropped_image))
            title = f"Text {len(bounding_boxes_data) + 1}: {text} - Confidence: {confidence}"
            bounding_box_data = {"title": title, "text": text, "confidence": confidence, "bbox": bbox}
            bounding_boxes_data.append(bounding_box_data)
            print(title)

    print(f"Số lượng bounding box được nhận diện: {len(bounding_boxes_data)}")

    cv2.imwrite("result_detection.jpg", clone_image_detection)
    cv2.waitKey(0)

    return bounding_boxes_data

if __name__ == "__main__":
    bounding_boxes_data = perform_text_detection_and_recognition(IMG_PATH)
    # Use bounding_boxes_data as needed, for example, to save it to a file or process further
    print("Bounding Boxes Data:", bounding_boxes_data)
