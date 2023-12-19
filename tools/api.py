from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile
import numpy as np
from PIL import Image
import cv2
from modules.text_detection import TextDetection
from modules.text_recognition import TextRecognition
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn


def perform_text_detection_and_recognition(image_detection):
    # Text Detection
    detector = TextDetection(device="cpu")
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


async def file2opencv(file):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def numpy_to_python(value):
    if isinstance(value, np.ndarray):
        return value.tolist()
    elif isinstance(value, np.generic):
        return value.item()
    else:
        return value



@app.post("/")
async def extract_info(img_front: UploadFile=File()):
    front_image = await file2opencv(img_front)
    data = perform_text_detection_and_recognition(front_image)

    # print(data)

    data = [{k: numpy_to_python(v) for k, v in item.items()} for item in data]
    json_compatible_item_data = jsonable_encoder(data)
    # data = {k: numpy_to_python(v) for k, v in data.items()}
    # json_compatible_item_data = jsonable_encoder(data)

    # print(json_compatible_item_data)

    return JSONResponse(content=json_compatible_item_data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, host="127.0.0.1", workers=1)
