import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

def EDA(path):
    """
    The EDA function takes a path to the csv file and returns a dictionary of the counts of each emotion.
    It also creates an image with the first two images from each emotion class.
    
    :param path: Specify the path of the csv file
    :return: A dictionary with the number of images per emotion
    :doc-author: Trelent
    """
    config = {
        "classes":   ["Angry",  "Disgust",  "Fear", "Happy",  "Sad",  "Surprise",  "Neutral"],
    }
    df = pd.read_csv(path)
    fig, ax = plt.subplots(1, len(config["classes"]), figsize=(20, 20))
    for i in range(len(config["classes"])):
        emotion = config["classes"][i]
        data = df[df.emotion == i].pixels.head(2).values
        face = [int(pixel) for pixel in data[0].split(' ')]
        face = np.asarray(face).reshape(48, 48)  # 3
        face = face.astype('float32')
        ax[i].imshow(face, cmap="gray")
        ax[i].set_title(emotion, size=18, color="#355")
    df_counted = dict(df.emotion.value_counts(sort=False))
    data_lbls_count = {}
    for i in range(len(config["classes"])):
        data_lbls_count[config["classes"][i]] = int(df_counted[i])

    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg',bbox_inches='tight')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode('ascii')
    return my_base64_jpgData,data_lbls_count
