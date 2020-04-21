import cv2
import numpy as np
import cropImage

#lower threshold for green
lower_green=np.array([37, 38, 70])
#upper threshold for green
upper_green=np.array([85, 255, 200])

def isDubleLine(pointCount):
    return (pointCount > 20000)

def getCoordenates(img):
    points = cv2.findNonZero(img)
    
    if (isDubleLine(points.__len__())):
        return

    avg = np.mean(points, axis=0)
    # assuming the resolutions of the image and screen are the following
    resImage = [40, int(cropImage.cropImg[0])]
    resScreen = [int(cropImage.cropImg[1]), int(cropImage.cropImg[0])]

    if (avg.__len__() == 1): 
        avg = avg[0]

    # points are in x,y coordinates
    pointInScreen = np.append((resScreen[0] / resImage[0]) * avg[0], (resScreen[1] / resImage[1]) * avg[1] )
    
    return pointInScreen

def informAction(x1, x2):
    halfLine = round( (x1 + x2)/2 )
    # print("HALF LINE GREEN " + str(halfLine))
    # print("GREEN " + str(int(cropImage.cropImg[2])))

    if (halfLine < int(cropImage.cropImg[2])/2):
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

def detectGreen(img, showImages = False):

    # img = cropImage.cropHorizontal(img)
    # cv2.imshow("imgCuted", img)

    kernel = np.ones((5,5), np.uint8) 
    morph = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    hsv = cv2.cvtColor(morph, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_green, upper_green)

    if (showImages):
        cv2.imshow("morphologyEx", morph)  
        cv2.imshow("cvtColor", hsv)
        cv2.imshow("mask", mask)


    if (validationMask(mask) == False):
        return 404

    ## slice the green
    imask = mask>0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    if (validationMask(green) == False):
        return 404

    if (showImages):
        cv2.imshow("green detect test", green)  

    point = getCoordenates(mask)

    if (point is None):
        return 0

    return informAction(point[0], point[1])



def test():
    print("Para o teste ser bem sucedido escolha uma das imagens da pasta /image:")
    print("greenBack")
    print("greenLeft")
    print("greenRight")
    fileName = input('Informe a imagem da pasta a ser verificada: ')

    img = cv2.imread(f'../image/{fileName}.jpg')

    action = detectGreen(img, True)

    if (action == 0):
        print("TWO GREEN STRIP")
    elif (action == 1):
        print("GREEN STRIP IN LEFT")
    elif (action == 2):
        print("GREEN STRIP IN RIGHT")
    else:
        print("DONT HAVE GREEN STRIP")

    cv2.waitKey(10000) 

test()
