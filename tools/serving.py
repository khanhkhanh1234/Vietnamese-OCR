from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile
import uvicorn
import numpy as np
import cv2
from modules.full_pipeline import FullPipeline

async def file2opencv(file):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img
app = FastAPI()
pipeline = FullPipeline(reconition_device="cpu")

# Đoạn này có thể thay đổi tùy theo cấu hình CORS của bạn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/")
async def extract_info(
    img_front: UploadFile=File(),
    img_back: UploadFile=File(),
    img_inner_left: UploadFile=File(),
    img_inner_right: UploadFile=File(),
    ):
    front_image = await file2opencv(img_front)
    back_image = await file2opencv(img_back)
    inner_left_image = await file2opencv(img_inner_left)
    inner_right_image = await file2opencv(img_inner_right)
    data = pipeline(front_image, inner_left_image, inner_right_image, back_image)
    print(data)
    # return data
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000, host="127.0.0.1", workers=1)

# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import uvicorn
# import numpy as np
# import cv2
# from modules.full_pipeline import FullPipeline

# class ImageData(BaseModel):
#     file: UploadFile

# app = FastAPI()
# pipeline = FullPipeline(reconition_device="cpu")
# async def file2opencv(file):
#     contents = await file.read()
#     nparr = np.fromstring(contents, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#     return img
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/")
# async def extract_info(
#     img_front: ImageData,
#     img_back: ImageData,
#     img_inner_left: ImageData,
#     img_inner_right: ImageData,
# ):
#     front_image = await file2opencv(img_front.file)
#     back_image = await file2opencv(img_back.file)
#     inner_left_image = await file2opencv(img_inner_left.file)
#     inner_right_image = await file2opencv(img_inner_right.file)
#     data = pipeline(front_image, inner_left_image, inner_right_image, back_image)
#     return data

# if __name__ == "__main__":
#     uvicorn.run(app, port=8000, host="127.0.0.1", workers=1)

