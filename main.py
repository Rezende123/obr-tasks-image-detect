import sys
import time
import cv2
sys.path.append('/home/felipe/Documentos/LineDetect/RaspLineDetect/lib/')

import lineDetect
import blackDetect
#import serialComunication

timeGap = time.time()
video_capture = cv2.VideoCapture(0)

def selectMode(mode, frame, timeGap):
    if (mode == 'LineDetect'):
        return lineDetect.followLine(frame, timeGap)
    elif (mode == 'TriangleDetect'):
        return blackDetect.detectBlack(frame, 10000)

def main():
    while True:

        global timeGap
        frame = video_capture.read()
        time.sleep(0.1)

        mode = serial.Read()
        response = selectMode(mode, frame, timeGap)
        
        serial.Write(response)

def test():
    global timeGap

    img = cv2.imread("/home/felipe/Documentos/LineDetect/RaspLineDetect/image/triangle.jpg")

    response = selectMode('TriangleDetect', img, timeGap)

    print('RESPONSE: ' + str(response))

test()