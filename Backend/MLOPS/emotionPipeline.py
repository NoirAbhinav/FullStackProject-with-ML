import sys
import os

sys.path.append(os.path.dirname(__file__))
from emotionDetect.code_artifacts.ETL import extraction, transformation, loading
import emotionDetect.code_artifacts.model_generate as generate
from emotionDetect.code_artifacts.EDA import EDA
from emotionDetect.code_artifacts.Model_info import Model_info


def get_modelInfo():
    return Model_info("MLOPS/emotion_detect/models/model_v1.h5")


def get_EDA():
    return EDA("MLOPS/emotion_detect/Data/fer2013.csv")


def get_data():
    return extraction("MLOPS/emotion_detect/Data/fer2013.csv")


def transform_data(emotion_data):
    return transformation(emotion_data)


def load_data(faces, emotions, width, height):
    return loading(faces, emotions, width, height)


def model_train(X_train, y_train, X_val, y_val, X_test, y_test, width, height, version):
    generate.Model_generate(
        X_train, y_train, X_val, y_val, X_test, y_test, width, height, version
    )
