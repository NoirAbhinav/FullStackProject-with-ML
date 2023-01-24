import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def extraction(path):
    emotion_data = pd.read_csv(path)
    print("Data Extracted")
    return emotion_data

def transformation(extracted_data):
    pixels = extracted_data['pixels'].tolist() # 1
    faces = []
    width, height = 48, 48
    for pixel_sequence in pixels:
        face = [int(pixel) for pixel in pixel_sequence.split(' ')] # 2
        face = np.asarray(face).reshape(width, height) # 3
        faces.append(face.astype('float32'))

    faces = np.asarray(faces)
    faces = np.expand_dims(faces, -1) # 6
    emotions = pd.get_dummies(extracted_data['emotion']).values # 7
    print("Data Transformed")
    return faces,emotions,width,height

def loading(faces,emotions,width,height):
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    X_train, X_test, y_train, y_test = train_test_split(faces, emotions, test_size=0.1, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.1, random_state=41)
    print("Data Loaded")
    return X_train, y_train,X_val,y_val, X_test,y_test,width,height,'v1'