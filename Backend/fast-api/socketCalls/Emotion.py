import cv2
import numpy as np
from PIL import Image
import base64
import io
from keras.models import load_model
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
model = load_model("MLOPS/emotion_detect/models/model_v1.h5")


def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))


def emotion_call(data):
    data = data.replace("data:image/jpeg;base64,", "")
    image = np.array(stringToImage(data))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
    return payload
