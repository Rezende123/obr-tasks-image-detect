import sys
import cv2
import numpy as np
sys.path.append('/home/felipe/Documentos/LineDetect/RaspLineDetect/lib/')

import lineDetect
import blackDetect
import ballTracking
#import serialComunication as serial

video_capture = cv2.VideoCapture(0)

def selectMode(mode, frame):
    if (mode == 1):
        return lineDetect.followLine(frame)
    elif (mode == 2):
        return blackDetect.detectBlack(frame, 10000)
    elif (mode == 3):
        return ballTracking.tracking(frame)

def main():
        while True:

                frame = video_capture.read()[1]
                time.sleep(0.1)

                mode = serial.Read()
                response = selectMode(mode, frame)
                
                serial.Write(response)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        # When everything done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()

#TESTES
def testTriangleDetect():
    img = cv2.imread("/home/felipe/Documentos/LineDetect/RaspLineDetect/image/triangle.jpg")
    cv2.imshow("imgCuted", img)

    response = selectMode(2, img)

    print('RESPONSE: ' + str(response))

def testSertial():
        serial.Write(b'3')
        
        read = serial.Read()
        print(read)

def testCam():
        while True:
                frame = video_capture.read()[1]

                print (frame)
                cv2.imshow('CAM', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        # When everything done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()

def testMain():
        while True:
                frame = video_capture.read()[1]

                response = lineDetect.followLine(frame)
                print(response)
                cv2.imshow('CAM', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        # When everything done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()

testMain()