from fastapi import Depends, FastAPI, UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import cv2
import io
import numpy as np
import datetime
import secrets

app = FastAPI()
security = HTTPBasic()


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
    # cv2.imwrite("inverted.jpg", inverted_image)
    res, im_png = cv2.imencode(".png", inverted_image)
    # return FileResponse("inverted.jpg")
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


@app.get("/time")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"test"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"test"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {datetime.datetime.now()}