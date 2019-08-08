import lib.lineDetect as lineDetect
import lib.serialComunication as serial

timeGap = time.time()
video_capture = cv2.VideoCapture(0)

while True:

    frame = video_capture.read()
    time.sleep(0.1)

    response = lineDetect.followLine(frame, timeGap)
    serial.Write(response)