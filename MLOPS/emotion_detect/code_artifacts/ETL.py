import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import time
import cv2
import base64


def extraction(path):
    inital_time = time.time()
    emotion_data = pd.read_csv(path)
    print("Data Extracted")
    head = emotion_data.head(5)
    head = head.to_dict(orient="records")
    ret_dict = {"Training": 0, "PublicTest": 0, "PrivateTest": 0}
    for i in ret_dict:
        ret_dict[i] = emotion_data["Usage"].to_list().count(i)
    final_time = time.time()
    time_taken = final_time - inital_time
    return head, ret_dict, time_taken, emotion_data


def transformation(extracted_data):
    pixels = extracted_data["pixels"].tolist()  # 1
    faces = []
    width, height = 48, 48
    inital_time = time.time()
    img_data = []
    ft = []
    i = 0
    for pixel_sequence in pixels:
        face = [int(pixel) for pixel in pixel_sequence.split(" ")]  # 2
        face = np.asarray(face).reshape(width, height)  # 3
        ft.append(face.tolist())
        faces.append(face.astype("float32"))
        if i < 5:
            retval, buffer = cv2.imencode(".jpg", face)
            payload = base64.b64encode(buffer).decode("ascii")
            img_data.append(payload)
            i = i + 1
    faces = np.asarray(faces)
    faces = np.expand_dims(faces, -1)  # 6
    emotions = pd.get_dummies(extracted_data["emotion"]).values  # 7
    df = pd.DataFrame(
        data={
            "emotions": extracted_data["emotion"].values[:5],
            "pixels": ft[:5],
            "Usage": extracted_data["Usage"].values[:5],
        }
    )
    ret_dict = {"Training": 0, "PublicTest": 0, "PrivateTest": 0}
    for i in ret_dict:
        ret_dict[i] = extracted_data["Usage"].to_list().count(i)
    df = df.to_dict(orient="records")
    final_time = time.time()
    time_taken = final_time - inital_time
    print("Data Transformed")
    return faces, emotions, width, height, df, time_taken, img_data, ret_dict


def loading(faces, emotions, width, height):
    X_train, X_test, y_train, y_test = train_test_split(
        faces, emotions, test_size=0.1, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.1, random_state=41
    )
    print("Data Loaded")
    return X_train, y_train, X_val, y_val, X_test, y_test, width, height, "v1"
