import cv2
import numpy as np
import cropImage

#lower threshold for black
lower_black=np.array([0, 0, 0])
#upper threshold for black
upper_black=np.array([180, 255, 30])

def isBlackCondition(pointCount, rangePixels):
    return (pointCount > rangePixels)

def validationMask(array):
    response = False

    average = np.mean(array, axis=0)
    
    for value in average:

        if (type(value).__name__ == 'ndarray'):
            value = np.mean(value, axis=0)

        if (value > 0.5):
            response = True

    return response

def detectBlack(img, rangePixels):

    imgCuted = cropImage.cropHorizontal(img)
    # cv2.imshow("imgCuted", imgCuted)

    kernel = np.ones((5,5), np.uint8) 
    morph = cv2.morphologyEx(imgCuted, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("morphologyEx", morph)  

    hsv = cv2.cvtColor(morph, cv2.COLOR_BGR2HSV)
    # cv2.imshow("cvtColor", hsv)

    mask = cv2.inRange(hsv, lower_black, upper_black)
    # cv2.imshow("mask", mask)

    if (validationMask(mask) == False):
        return 404

    ## slice the black
    imask = mask>0
    black = np.zeros_like(imgCuted, np.uint8)
    black[imask] = imgCuted[imask]

    if (validationMask(black) == False):
        return 404

    # cv2.imshow("black detect test", black)
    
    points = cv2.findNonZero(mask)
    
    if (isBlackCondition(points.__len__(), rangePixels)):
        return -255

    return 404
