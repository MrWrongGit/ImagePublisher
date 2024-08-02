import cv2
import time
from webserver import imageUpdateHelper

# get input
caps = [
    cv2.VideoCapture("../resource/demo.mp4"),
    cv2.VideoCapture("../resource/robot.mp4"),
    cv2.VideoCapture("../resource/video.mp4")
]
print("Start to read video")

while True:
    fail_count = 0
    for idx, cap in enumerate(caps):
        # get image frame
        ret, frame = cap.read()
        if ret == False:
            fail_count += 1
            continue
        # change frame size
        frame = cv2.resize(frame, (640, 360))
        # compress and send through http to web server
        _, compressed_result = cv2.imencode('.jpg', frame)
        imageUpdateHelper(compressed_result, idx)
    # all finish
    if fail_count == len(caps):
        break
    # time.sleep(0.02)

# realease
for cap in caps:
    cap.release()