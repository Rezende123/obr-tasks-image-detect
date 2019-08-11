import lib.lineDetect as lineDetect
import lib.blackDetect as blackDetect
import lib.serialComunication as serial

timeGap = time.time()
video_capture = cv2.VideoCapture(0)

def selectMode(mode, frame, timeGap):
    if (mode == 'LineDetect'):
        return lineDetect.followLine(frame, timeGap)
    elif (mode == 'TriangleDetect'):
        return blackDetect.detectBlack(frame, 10000)

while True:

    frame = video_capture.read()
    time.sleep(0.1)

    mode = serial.Read()
    response = selectMode(mode, frame, timeGap)
    
    serial.Write(response)