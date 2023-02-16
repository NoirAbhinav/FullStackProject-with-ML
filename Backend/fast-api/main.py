import uvicorn
from fastapi import FastAPI, WebSocket
import uvicorn
import cv2
import base64
import time
import numpy as np
from pydantic import BaseModel
from MLOPS import emotionPipeline as emotion_pipes
from socketCalls import Emotion
from socketCalls import HandTrack

from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from MLOPS import covidmaskPipeline as cvmask_pipes

origins = ["*"]
states = {
    "eda": {"Data": [], "users": [], "module": ""},
    "modelInfo": {"Data": [], "users": [], "module": ""},
}


app = FastAPI(title="WebSocket Example")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class recvData(BaseModel):
    ml_module: str
    user_id: str


@app.post("/model/close")
async def end_session(data: recvData):
    print(data)
    print("session closed")
    for i in states.values():
        try:
            i["users"].remove(data.user_id)
        except:
            print("No User found")
    return "Session Closed"


@app.post("/model/EDA")
async def EDA(data: recvData):
    print("EDA Called:")
    if (
        data.ml_module == "emotions"
        and states["eda"]["module"] == "emotion"
        and data.user_id in states["eda"]["users"]
    ):
        return states["eda"]["Data"]

    else:
        ret_val = emotion_pipes.get_EDA()
        states["eda"]["Data"] = ret_val
        states["eda"]["module"] = "emotion"
        states["eda"]["users"].append(data.user_id)
        # print(ret_val[4:7])
        return ret_val


def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))


@app.post("/model/modelInfo")
async def Model_Info(data: recvData):
    print("Model Info Called:")
    if (
        data.ml_module == "emotions"
        and states["modelInfo"]["module"] == "emotion"
        and data.user_id in states["modelInfo"]["users"]
    ):
        return states["modelInfo"]["Data"]

    else:
        ret_val = emotion_pipes.get_modelInfo()
        states["modelInfo"]["Data"] = ret_val
        states["modelInfo"]["module"] = "emotion"
        states["modelInfo"]["users"].append(data.user_id)
        # print(ret_val[4:7])
        return ret_val


@app.websocket("/handws")
async def handtracking(websocket: WebSocket):
    print("hi")
    await websocket.accept()
    while 1:
        data = await websocket.receive_text()
        payload = HandTrack.handTrack_call(data)
        await websocket.send_text(payload)
        if data == "closed":
            break


@app.websocket("/covmaskws")
async def covidmaskTracker(websocket: WebSocket):
    print("Accepting client connection...")
    await websocket.accept()
    while 1:
        data = await websocket.receive_text()
        if data == "closed":
            break
        payload = cvmask_pipes.get_mask_detect(data)
        await websocket.send_text(payload)


@app.websocket("/emotionws")
async def emotion_socket(websocket: WebSocket):
    print("Accepting client connection...")
    await websocket.accept()
    while 1:
        data = await websocket.receive_text()
        if data == "closed":
            break
        payload = Emotion.emotion_call(data)
        await websocket.send_text(payload)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="localhost", port=8000, log_level="info", reload="True"
    )
