import cv2
import numpy as np
import HandTrackingModule as htm
import time
#import autopy

wCam, hCam = 640, 480
pTime=0
detector = htm.handDetector(maxHands=1)

cap = cv2.VideoCapture(-0)
cap.set(3, wCam)
cap.set(4, hCam)

while True:
    success, img = cap.read()
    img=detector.findHands(img)
    lmList =detector.findPos(img)
    print(lmList)

    if len(lmList)!=0:
        x1, y1 = lmList[8][1],lmList[8][2]
        x2, y2 = lmList[12][1],lmList[12][2]

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(480,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()




