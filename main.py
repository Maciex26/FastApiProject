from fastapi import Depends, FastAPI, UploadFile, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import cv2
import io
import numpy as np
import datetime
import secrets

fake_users_db = {
    "user": {
        "username": "user",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}

app = FastAPI()

security = HTTPBasic()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"stanleyjobson"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"swordfish"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get("/")
async def root():
    return {"message": "Hello World"}


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


@app.post("/time")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # return {"access_token": user.username, "token_type": "bearer"}
    return {datetime.datetime.now()}


@app.get("/users/me")
def read_current_user(username: str = Depends(get_current_username)):
    return {"username": username}