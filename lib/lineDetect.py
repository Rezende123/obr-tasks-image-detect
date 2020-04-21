import sys
import time
import cv2
import numpy as np
import os
import greenDetect
import blackDetect
import imageAjust
import cropImage

Kernel_size=15
low_threshold=40
high_threshold=120

rho=10
threshold=15
theta=np.pi/180
minLineLength=10
maxLineGap=1

def imageFilter(image, showImages = False):

    # image = cropImage.cropHorizontal(image)
    # cv2.imshow("imageCuted", image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    kernel = np.ones((5,5), np.uint8) 
    opening = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

    edged = cv2.Canny(opening, low_threshold, high_threshold)

    if (showImages):
        cv2.imshow("cvtColor", gray)
        cv2.imshow("morphologyEx", opening)
        cv2.imshow("canny", edged)

        print("CHEGOU")

    return edged

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
    else:
        return _response

def followLine(img):
    preparedImage = imageAjust.prepare(img)

    response = greenDetect.detectGreen(preparedImage)

    if (response == 404):
        response = blackDetect.detectBlack(preparedImage, 15000)

    if (response == 404):
        imageFiltred = imageFilter(preparedImage)
        lines = cv2.HoughLinesP(imageFiltred,rho,theta,threshold,minLineLength,maxLineGap)

        #Draw lines on input image
        if(lines is not None):
            for x1,y1,x2,y2 in lines[0]:
                cv2.line(imageFiltred,(x1,y1),(x2,y2),(0,255,0),2)
                response = defineAction( x1, x2 )

        else:
            return 404
    else:
        response = convertDetectGreenValue(response)

    return response


def printAction(_response):
    if (_response == 0):
        return "POINT[%d] AEE, SIGA EM FRENTE" % (_response)
    elif (_response < 0 and _response >= -100):
        return "POINT[%d] GO TO RIGHT VEI!" % (_response)
    elif (_response > 0 and _response <= 100):
        return "POINT[%d] GO TO LEFT VEI!" % (_response)
    elif (_response == 255):
        return "TWO GREEN, HALF TURN VEI!"
    elif (_response == -255):
        return "BLACK CONDITION, TEST THE FRONT VEI!"
    elif (_response == -110):
        return "GREEN, LEFT TURN VEI!"
    elif (_response == 110):
        return "GREEN, RIGHT TURN VEI!"
    elif (_response == 404):
        return "LINE NOT FOUND, RETURN PLEASE"

def main ():    
    ## Read
    img = cv2.imread("../image/cameraGreenRight.jpg")

    response = followLine(img)

    print('RESPONSE: ' + str(response))
    action = printAction(response)
    print(action)

    cv2.waitKey(10000)

def calibration():
    # Read image
    im = cv2.imread("../image/cameraLine.jpg")
    preparedImage = imageAjust.prepare(im)
     
    # Select ROI
    cropImg = cv2.selectROI(preparedImage)
    print(cropImg)

    # Crop image
    imCrop = preparedImage[int(cropImg[1]):int(cropImg[1]+cropImg[3]), int(cropImg[0]):int(cropImg[0]+cropImg[2])]
 
    # Display cropped image
    # cv2.imshow("Image", imCrop)

    cv2.waitKey(10000)

def test():
    print("Para o teste ser bem sucedido escolha uma das imagens da pasta /image:")
    print("simpleLine")
    print("simpleLine2")
    print("cameraLine")
    fileName = input('Informe a imagem da pasta a ser verificada: ')

    img = cv2.imread(f'../image/{fileName}.jpg')

    img = imageFilter(img, True)
    lines = cv2.HoughLinesP(img,rho,theta,threshold,minLineLength,maxLineGap)
    
    cv2.imshow("HoughLinesP", lines)

    response = 404
    #Draw lines on input image
    if(lines is not None):
        for x1,y1,x2,y2 in lines[0]:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
            response = defineAction( x1, x2 )
    
    
    print(f'Response: {response}')

    cv2.waitKey(10000)

test()