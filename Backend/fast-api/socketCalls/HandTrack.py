from NonMLProjects.HandGestureMaster import HandTrackingModule as htm
import cv2
import numpy as np
from PIL import Image
import base64
import io
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

tipIds = [4, 8, 12, 16, 20]
NumCount = 0
fingers = []
detector = htm.handDetector(detConf=0.5)


def stringToImage(base64_string):
    imgdata = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(imgdata))


def handTrack_call(data):
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
    return payload
