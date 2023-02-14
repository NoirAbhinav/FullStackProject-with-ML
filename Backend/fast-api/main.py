import uvicorn
from fastapi import FastAPI, WebSocket
import uvicorn
import cv2
import base64
import time
import numpy as np
from pydantic import BaseModel
from MLOPS import emotion_pipeline as emotion_pipes
from MLOPS import covidmask_pipeline as cvmask_pipes
from keras.models import load_model
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from NonMLProjects.HandGestureMaster import HandTrackingModule as htm

import os

print(os.getcwd())

model = load_model("MLOPS/emotion_detect/models/model_v1.h5")
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
origins = ["*"]
states = {
    "eda": {"Data": [], "users": [], "module": ""},
    "modelInfo": {"Data": [], "users": [], "module": ""},
}
detector = htm.handDetector(detConf=0.5)

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
    tipIds = [4, 8, 12, 16, 20]
    NumCount = 0
    fingers = []
    while 1:
        data = await websocket.receive_text()
        data = data.replace("data:image/jpeg;base64,", "")
        img = np.array(stringToImage(data))
        img = detector.findHands(img)
        if detector.DetHandNo(img) == 0:
            lmList1 = detector.findPos(img, draw=False)
            print(lmList1)
            if len(lmList1) != 0:
                if lmList1[4][1] > lmList1[3][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                for id in range(1, 5):
                    if lmList1[tipIds[id]][2] < lmList1[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
        if detector.DetHandNo(img) == 1:
            lmList2 = detector.findPos(img, draw=False)
            if len(lmList2) != 0:
                if lmList2[4][1] < lmList2[3][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                for id in range(1, 5):
                    if lmList2[tipIds[id]][2] < lmList2[tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

        NumCount = fingers.count(1)
        # cTime = time.time()
        # fps = 1 / (cTime - pTime)
        # pTime = cTime
        # cv2.putText(
        #     img,
        #     f"FPS:{int(fps)}",
        #     (480, 50),
        #     cv2.FONT_HERSHEY_COMPLEX,
        #     1,
        #     (255, 0, 0),
        #     2,
        # )
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        retval, buffer = cv2.imencode(".jpg", img)
        payload = base64.b64encode(buffer).decode("ascii")
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
        payload = cvmask_pipes()
        await websocket.send_text(payload)


@app.websocket("/emotionws")
async def emotion_socket(websocket: WebSocket):
    print("Accepting client connection...")
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    await websocket.accept()
    while 1:
        data = await websocket.receive_text()
        if data == "closed":
            break
        data = data.replace("data:image/jpeg;base64,", "")
        image = np.array(stringToImage(data))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        print(gray)
        emotion_dict = {
            0: "Angry",
            1: "Disgust",
            2: "Fear",
            3: "Happy",
            4: "Sad",
            5: "Surprise",
            6: "Neutral",
        }
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 1)
            roi_gray = gray[y : y + h, x : x + w]
            cropped_img = np.expand_dims(
                np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0
            )
            cv2.normalize(
                cropped_img,
                cropped_img,
                alpha=0,
                beta=1,
                norm_type=cv2.NORM_L2,
                dtype=cv2.CV_32F,
            )
            prediction = model.predict(cropped_img)
            cv2.putText(
                image,
                emotion_dict[int(np.argmax(prediction))],
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                1,
                cv2.LINE_AA,
            )
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        retval, buffer = cv2.imencode(".jpg", image)
        payload = base64.b64encode(buffer).decode("ascii")
        await websocket.send_text(payload)


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="localhost", port=8000, log_level="info", reload="True"
    )
