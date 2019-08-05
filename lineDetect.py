import sys
import time
import cv2
import numpy as np
import os
import greenDetect

WIDTH = 600
HEIGHT = 400

Kernel_size=15
low_threshold=40
high_threshold=120

rho=10
threshold=15
theta=np.pi/180
minLineLength=10
maxLineGap=1
timeGap: float = time.time()

def imageFilter(image):

    imgCuted = image[0:WIDTH, HEIGHT:WIDTH]
    cv2.imshow("imgCuted", imgCuted)

    gray = cv2.cvtColor(imgCuted, cv2.COLOR_BGR2HSV)
    cv2.imshow("cvtColor", gray)

    kernel = np.ones((5,5), np.uint8) 
    opening = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("morphologyEx", opening)    

    edged = cv2.Canny(opening, low_threshold, high_threshold)
    cv2.imshow("canny", edged)    

    return edged

def isGapLine(line, timeGap):
    currentTime = time.time() - timeGap
    limitTime = 5

    if (currentTime <= limitTime):
        print("It's gap")
        return 0
    else:
        print("Line not found, return please")
        return None

def defineAction( x1, x2 ):
    halfLine = round( (x1 + x2)/2 )
    sizeOfParts = 8
    target = 55

    quadOfLine = round(halfLine / sizeOfParts)

    return target - quadOfLine 

def convertDetectGreenValue(_response):
    if (_response == 0):
        return 255
    elif (_response == 1):
        return -110
    elif (_response == 2):
        return 110

def followLine(img, timeGap):
    response: int

    response = greenDetect.detectGreen(img)

    if (response is None):
        imageFiltred = imageFilter(img)
        lines = cv2.HoughLinesP(imageFiltred,rho,theta,threshold,minLineLength,maxLineGap)

        #Draw lines on input image
        if(lines is not None):
            timeGap = time.time()

            for x1,y1,x2,y2 in lines[0]:
                cv2.line(imageFiltred,(x1,y1),(x2,y2),(0,255,0),2)
                response = defineAction( x1, x2 )

        else:
            # timeGap = timeGap  
            response = isGapLine(lines, timeGap)
    else:
        response = convertDetectGreenValue(response)

    return response


def printAction(_response):
    if (_response == 0):
        return "POINT[%d] AEE, SIGA EM FRENTE" % (_response)
    elif (_response < 0 and _response >= -100):
        return "POINT[%d] GO TO RIGHT VEI" % (_response)
    elif (_response > 0 and _response <= 100):
        return "POINT[%d] GO TO LEFT VEI" % (_response)
    elif (_response == 255):
        return "TWO GREEN, HALF TURN VEI"
    elif (_response == -110):
        return "GREEN, LEFT TURN VEI"
    elif (_response == 110):
        return "GREEN, RIGHT TURN VEI"
    elif (_response == None):
        return "LINE NOT FOUND, RETURN PLEASE"

## Read
img = cv2.imread("greenBack.jpg")

response = followLine(img, timeGap)

action = printAction(response)
print('RESPONSE: ' + str(response))
print(action)

cv2.waitKey(10000)