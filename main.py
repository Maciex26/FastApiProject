from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, Response
import cv2
import numpy as np

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/monke")
async def root():
    return {"MONKE"}


@app.get("/prime/{number}")
async def prime(number: int):
    if 1 <= number <= 9223372036854775807:
        for i in range(2, int(number ** 0.5) + 1):
            if (number % i) == 0:
                return {f"{number} isn't prime"}
        return {f"{number} is prime"}
    else:
        return {"Input is not supported"}


@app.post("/picture/invert")
async def invert(file: UploadFile):
    contents = await file.read()
    nparray = np.fromstring(contents, np.uint8)
    # image = cv2.imread(contents, 0)
    # inverted_image = cv2.bitwise_not(image)
    # inverted_image = np.invert(nparray)
    img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
    inverted_image = cv2.bitwise_not(img)
    cv2.imwrite("inverted.jpg", inverted_image)
    return FileResponse("inverted.jpg")
    # return Response(content=inverted_image, media_type="image/jpg")

