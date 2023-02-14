import cv2
import time
import numpy as np 
import math
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
import HandTrackingModule as htm 
####################################
wCam,Hcam=640,480
####################################
cap=cv2.VideoCapture(-0)
cap.set(3,wCam)
cap.set(4,Hcam)
pTime=0

detector=htm.handDetector(detConf=0.75)
devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume = cast(interface ,POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(0,None)
minVol=volRange[0]
maxVol=volRange[1]
vol=0
volB=400
volP=0
while True:
    success, img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPos(img,draw=False)
    if(len(lmList)!=0):
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)
        #print(length)
        vol=np.interp(length,[15,150],[minVol,maxVol])
        volB=np.interp(length,[15,150],[400,150])
        volP=np.interp(length,[15,150],[0,100])
        volume.SetMasterVolumeLevel(vol,None)
        print(vol)

        if length<50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

    cv2.rectangle(img,(30,130),(85,400),(0,255,0),3)
    cv2.rectangle(img,(30,int(volB)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img,f'Per:{int(volP)}',(40,120),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(480,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    cv2.imshow("Img",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
