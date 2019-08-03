import cv2
import numpy as np

WIDTH = 600
HEIGHT = 400
#lower threshold for green
lower_green=np.array([36, 35, 35])
#upper threshold for green
upper_green=np.array([100, 255, 255])

def isDubleLine(pointCount):
    return (pointCount > 12000)

def getCoordenates(img):
    points = cv2.findNonZero(img)
    
    if (isDubleLine(points.__len__())):
        print("IS DUBLE GREEN")
        return

    avg = np.mean(points, axis=0)
    # assuming the resolutions of the image and screen are the following
    resImage = [40, WIDTH]
    resScreen = [HEIGHT, WIDTH]

    if (avg.__len__() == 1): 
        avg = avg[0]

    # points are in x,y coordinates
    pointInScreen = np.append((resScreen[0] / resImage[0]) * avg[0], (resScreen[1] / resImage[1]) * avg[1] )
    
    return pointInScreen

def informAction(x1, x2):
    halfLine = round( (x1 + x2)/2 )
    print("HALF LINE GREEN " + str(halfLine))

    if (halfLine > WIDTH/2):
        print("VÁ PARA A ESQUERDA")
    else:
        print("VÁ PARA A DIREITA")

def validationMask(mask):
    response = False

    for _mask in mask:
        for value in _mask:
            if (value != 0):
                response = True

    return response

def detectGreen(img, gray):

    mask = cv2.inRange(gray, lower_green, upper_green)
    # cv2.imshow("mask", mask)

    if (validationMask(mask) == False):
        return

    ## slice the green
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    cv2.imshow("green detect test", green)

    opening = cv2.morphologyEx(green, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("morphologyEx", opening)    

    point = getCoordenates(mask)

    if (point is None):
        return

    informAction(point[0], point[1])



## Read
img = cv2.imread("greenBack.jpg")

imgCuted = img[0:WIDTH, HEIGHT:WIDTH]
cv2.imshow("imgCuted", imgCuted)

kernel = np.ones((5,5), np.uint8) 

gray = cv2.cvtColor(imgCuted, cv2.COLOR_BGR2HSV)
cv2.imshow("cvtColor", gray)

detectGreen(imgCuted, gray)

cv2.waitKey(0) 

