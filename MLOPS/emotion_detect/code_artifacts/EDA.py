import pandas as pd
import numpy as np
import io
import base64
import cv2


def EDA(path):
    """
    The EDA function takes a path to the csv file and returns a dictionary of the counts of each emotion.
    It also creates an image with the first two images from each emotion class.

    :param path: Specify the path of the csv file
    :return: A dictionary with the number of images per emotion
    :doc-author: Trelent
    """
    config = {
        "classes": ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"],
    }
    df = pd.read_csv(path)
    emotion_data = []
    pixels = df["pixels"].tolist()[:5]
    img_data = []
    ft = []
    faces = []
    for pixel_sequence in pixels:
        face = [int(pixel) for pixel in pixel_sequence.split(" ")]  # 2
        face = np.asarray(face).reshape(48, 48)  # 3
        ft.append(face.tolist())
        faces.append(face.astype("float32"))
        retval, buffer = cv2.imencode(".jpg", face)
        payload = base64.b64encode(buffer).decode("ascii")
        img_data.append(payload)
    for i in range(len(config["classes"])):
        data = df[df.emotion == i].pixels.head(2).values
        face = [int(pixel) for pixel in data[0].split(" ")]
        face = np.asarray(face).reshape(48, 48)  # 3
        face = face.astype("float32")
        retval, buffer = cv2.imencode(".jpg", face)
        payload = base64.b64encode(buffer).decode("ascii")
        emotion_data.append(payload)
    df_counted = dict(df.emotion.value_counts(sort=False))
    df_ret = pd.DataFrame(
        data={
            "emotions": df["emotion"].values[:5],
            "pixels": ft[:5],
            "Usage": df["Usage"].values[:5],
        }
    )
    df_ret = df_ret.to_dict(orient="records")
    data_lbls_count = {}
    ret_dict = {"Training": 0, "PublicTest": 0, "PrivateTest": 0}
    for i in ret_dict:
        ret_dict[i] = int(df["Usage"].to_list().count(i))
    for i in range(len(config["classes"])):
        data_lbls_count[config["classes"][i]] = int(df_counted[i])
    print(emotion_data, data_lbls_count, df_ret, img_data, ret_dict)
    print(data_lbls_count)
    return df_ret, img_data, ret_dict, emotion_data, data_lbls_count


# EDA('../Data/fer2013.csv')
