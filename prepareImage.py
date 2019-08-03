import cv2
import numpy as np

WIDTH = 600
HEIGHT = 400
#lower threshold for green
lower_green=np.array([36, 35, 35])
#upper threshold for green
upper_green=np.array([100, 255, 255])

def getCoordenates(img):
    points = cv2.findNonZero(img)
    avg = np.mean(points, axis=1)
    # assuming the resolutions of the image and screen are the following
    resImage = [40, WIDTH]
    resScreen = [HEIGHT, WIDTH]

    # points are in x,y coordinates
    pointInScreen = np.append((resScreen[0] / resImage[0]) * avg[0], (resScreen[1] / resImage[1]) * avg[1] )
    
    return pointInScreen

def informAction(y1, y2):
    halfLine = round( (y1 + y2)/2 )

    if (halfLine > WIDTH/2):
        print("VÁ PARA A ESQUERDA")
    else:
        print("VÁ PARA A DIREITA")

def detectGreen(img, gray):

    mask = cv2.inRange(gray, lower_green, upper_green)
    cv2.imshow("mask", mask)

    print(mask)
    ## slice the green
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    cv2.imshow("green detect test", green)

    opening = cv2.morphologyEx(green, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("morphologyEx", opening)    

    point = getCoordenates(mask)
    informAction(point[0], point[2])
    print(point)



## Read
img = cv2.imread("green.jpg")

imgCuted = img[0:WIDTH, HEIGHT:WIDTH]

kernel = np.ones((5,5), np.uint8) 

gray = cv2.cvtColor(imgCuted, cv2.COLOR_BGR2HSV)
cv2.imshow("cvtColor", gray)

detectGreen(imgCuted, gray)

cv2.waitKey(0) 
# edged = cv2.Canny(blurred, low_threshold, high_threshold)
# cv2.imshow("Canny", edged)

