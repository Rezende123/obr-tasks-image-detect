import cv2
import numpy as np


minLineLength = 10
maxLineGap = 1

#Initialize camera
video_capture = cv2.VideoCapture(0)

while True:
    # CAPTURE FRAME-BY-FRAME
    frame = video_capture.read()
    time.sleep(0.1)

    # Prepare image
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    # DETECT HOUGH LINES
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)

    for x1,y1,x2,y2 in lines[0]:
        cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.putText(frame,'lines_detected ALEK',(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),1)

    # cv2.imshow("line detect test", frame)