import sys,os
from fastapi import FastAPI, WebSocket
import random
import uvicorn
import cv2
import base64
import time
import numpy as np
sys.path.append(str(os.environ.get('CHECKPATH')))
# from MLOPS import pipeline as pipes
from keras.models import load_model
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

model = load_model('/home/abhinav/Personal_project/FullStackProject-with-ML/MLOPS/emotion_detect/models/model_v1.h5')

app = FastAPI(title='WebSocket Example')
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    cap = cv2.VideoCapture(0)
    await websocket.accept()
    i=0
    intial_time = time.time()
    while True:
        try:
            if time.time() - intial_time <= 0.1:
                continue
            intial_time = time.time()
            ret,frame = cap.read()
            emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fear", 3: "Happy", 4: "Sad", 5: "Surprise", 6: "Neutral"}
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                roi_gray = gray[y:y + h, x:x + w]
                cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
                cv2.normalize(cropped_img, cropped_img, alpha=0, beta=1, norm_type=cv2.NORM_L2, dtype=cv2.CV_32F)
                prediction = model.predict(cropped_img)
                cv2.putText(frame, emotion_dict[int(np.argmax(prediction))], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

            retval, buffer = cv2.imencode('.jpg', frame)
            payload = base64.b64encode(buffer).decode('ascii')
            await websocket.send_text(payload)
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info",reload='True')