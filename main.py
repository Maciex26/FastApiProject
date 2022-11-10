from fastapi import FastAPI
import cv2

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


# @app.post("/picture/invert")
