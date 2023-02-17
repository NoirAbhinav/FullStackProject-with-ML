import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import imutils
from PIL import Image
import cv2
import io
import base64

prototxtPath = os.path.sep.join(
    [
        "MLOPS/covidMask/Face",
        "deploy.prototxt",
    ]
)
weightsPath = os.path.sep.join(
    [
        "MLOPS/covidMask/Face",
        "res10_300x300_ssd_iter_140000.caffemodel",
    ]
)

faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
maskNet = load_model("MLOPS/covidMask/Model")


def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))


def detect_and_predict_mask(frame, faceNet, maskNet):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    faceNet.setInput(blob)
    detections = faceNet.forward()
    faces = []
    locs = []
    preds = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.7:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)
            faces.append(face)
            locs.append((startX, startY, endX, endY))
    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)
    return (locs, preds)


def get_mask_detect(data):
    data = data.replace("data:image/jpeg;base64,", "")
    frame = np.array(stringToImage(data))
    frame = imutils.resize(frame, width=400)
    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
    if locs or preds:
        (startX, startY, endX, endY) = locs[0]
        (mask, withoutMask) = preds[0]
        label = "Mask" if mask > withoutMask else "No Mask"
        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
        cv2.putText(
            frame,
            label,
            (startX, startY - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            color,
            2,
        )
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    retval, buffer = cv2.imencode(".jpg", img)
    payload = base64.b64encode(buffer).decode("ascii")
    return payload
