import cv2
import time
import os
import numpy as np
import HandTrackingModule as htm


wCam, hCam = 640, 480

cap = cv2.VideoCapture(-0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(detConf=0.7)


vol = 0
pTime = 0
cTime = 0
tipIds = [4, 8, 12, 16, 20]
NumCount = 0
fingers = []

while True:
    sucess, img = cap.read()
    img = detector.findHands(img)
    fingers1 = []

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
    cv2.putText(
        img,
        f"Num:{int(NumCount)}",
        (10, 50),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (255, 0, 0),
        2,
    )
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(
        img, f"FPS:{int(fps)}", (480, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2
    )
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
