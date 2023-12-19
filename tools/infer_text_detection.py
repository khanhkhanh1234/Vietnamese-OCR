from modules.text_detection import TextDetection    
import cv2

IMG_PATH = r"samples/hm1.jpg"

if __name__ == "__main__":
    detector = TextDetection(device="cpu")
    
    image = cv2.imread(IMG_PATH)
    clone_image = image.copy()
    image = image[:, :, ::-1]
    clone_image = image.copy()

    bounding_box_count = 0  # Đếm số lượng bounding box

    for i, line in enumerate(detector(image)):
        line_text = ""
        for bbox, image in line:
            clone_image = cv2.polylines(clone_image, [bbox], isClosed=True, color=(255, 0, 0), thickness=1)
            bounding_box_count += 1
    
    print(f"Số lượng bounding box được nhận diện: {bounding_box_count}")

    cv2.imshow("result", clone_image)
    cv2.imwrite("result.jpg", clone_image)
    cv2.waitKey(0)