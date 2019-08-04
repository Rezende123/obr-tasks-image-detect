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
        return 1
    else:
        return 2

def validationMask(array):
    response = False

    average = np.mean(array, axis=0)
    
    for value in average:

        if (type(value).__name__ == 'ndarray'):
            value = np.mean(value, axis=0)

        if (value > 0.5):
            response = True

    return response

def detectGreen(img):

    imgCuted = img[0:WIDTH, HEIGHT:WIDTH]
    cv2.imshow("imgCuted", imgCuted)

    gray = cv2.cvtColor(imgCuted, cv2.COLOR_BGR2HSV)
    cv2.imshow("cvtColor", gray)

    mask = cv2.inRange(gray, lower_green, upper_green)
    # cv2.imshow("mask", mask)

    if (validationMask(mask) == False):
        return

    ## slice the green
    imask = mask>0
    green = np.zeros_like(imgCuted, np.uint8)
    green[imask] = imgCuted[imask]

    if (validationMask(green) == False):
        return

    cv2.imshow("green detect test", green)

    kernel = np.ones((5,5), np.uint8) 
    opening = cv2.morphologyEx(green, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("morphologyEx", opening)    

    point = getCoordenates(mask)

    if (point is None):
        return 0

    return informAction(point[0], point[1])



## Read
img = cv2.imread("greenBack.jpg")

action = detectGreen(img)

if (action == 0):
    print("TWO GREEN STRIP")
elif (action == 1):
    print("GREEN STRIP IN LEFT")
elif (action == 2):
    print("GREEN STRIP IN RIGHT")
else:
    print("DONT HAVE GREEN STRIP")

cv2.waitKey(10000) 

