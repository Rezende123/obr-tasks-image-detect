import sys
import time
import cv2
sys.path.append('/home/felipe/Documentos/LineDetect/RaspLineDetect/lib/')

import lineDetect
import blackDetect
import serialComunication as serial

timeGap = time.time()
video_capture = cv2.VideoCapture(0)

def selectMode(mode, frame, timeGap):
    if (mode == 1):
        return lineDetect.followLine(frame, timeGap)
    elif (mode == 2):
        return blackDetect.detectBlack(frame, 10000)

def main():
    while True:

        global timeGap
        frame = video_capture.read()
        time.sleep(0.1)

        mode = serial.Read()
        response = selectMode(mode, frame, timeGap)
        
        serial.Write(response)

def testTriangleDetect():
    global timeGap

    img = cv2.imread("/home/felipe/Documentos/LineDetect/RaspLineDetect/image/triangle.jpg")
    cv2.imshow("imgCuted", img)

    response = selectMode('TriangleDetect', img, timeGap)

    print('RESPONSE: ' + str(response))

def testSertial():
        serial.Write(b'3')
        
        read = serial.Read()
        print(read)

testSertial()