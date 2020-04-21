import cv2
import numpy as np
import cropImage

low_threshold=40
high_threshold=120

def tracking(img):
    response = 404
    img = cropImage.cropVertical(img)

    blur = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(blur,cv2.COLOR_GRAY2BGR)
    # cv2.imshow('gray',cimg)

    kernel = np.ones((5,5), np.uint8) 
    morpho = cv2.morphologyEx(cimg, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow("morphologyEx", morpho)    

    edged = cv2.Canny(morpho, low_threshold, high_threshold)
    # cv2.imshow("edged", edged)    

    circles = cv2.HoughCircles(edged,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=30,minRadius=0,maxRadius=0)

    if (circles is not None):
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
        

        # cv2.imshow('detected circles',cimg)

        response = -255
    
    # if cv2.waitKey(15000) & 0xFF == ord('q'):
    #     cv2.destroyAllWindows()

    return response


def test():
    img = cv2.imread("/home/felipe/Documentos/LineDetect/RaspLineDetect/image/ball_gray.jpg",0)

    response = tracking(img)

    if (response == -255):
        print("HAVE BALL")
    else:
        print("DON'T HAVE BALL")

test()