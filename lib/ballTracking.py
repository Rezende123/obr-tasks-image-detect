import cv2
import numpy as np
import cropImage

low_threshold=40
high_threshold=120

def tracking(img, showImages = False):
    response = 404
    # img = cropImage.cropVertical(img)

    blur = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(blur,cv2.COLOR_GRAY2BGR)

    kernel = np.ones((5,5), np.uint8) 
    morpho = cv2.morphologyEx(cimg, cv2.MORPH_CLOSE, kernel)

    edged = cv2.Canny(morpho, low_threshold, high_threshold)

    circles = cv2.HoughCircles(edged,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=0)

    if (circles is not None):
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
        


        response = -255

    if (showImages):
        cv2.imshow("morphologyEx", morpho)    
        cv2.imshow("edged", edged)    
        cv2.imshow('detected circles',cimg)

        if cv2.waitKey(15000) & 0xFF == ord('q'):
            cv2.destroyAllWindows()


    return response


def test():
    print("Para o teste ser bem sucedido escolha uma das imagens da pasta /image:")
    print("ball_gray")
    print("ball_gray_alone")
    print("ball_gray_triangle")
    print("ball_black")
    print("ball_black_alone")
    print("ball_black_triangle")
    fileName = input('Informe a imagem da pasta a ser verificada: ')

    img = cv2.imread(f'../image/{fileName}.jpg',0)

    response = tracking(img, True)

    if (response == -255):
        print("HAVE BALL")
    else:
        print("DON'T HAVE BALL")

test()