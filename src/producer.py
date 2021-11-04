import cv2
import time
from webserver import imageUpdateHelper

# get input
cap = cv2.VideoCapture("../resource/demo.mp4")

while True:
    # get image
    ret, frame = cap.read()
    if ret == False:
        break
    
    # image process
    #---- put code here ----#

    # compress and send through http to web server
    _, compressed_result = cv2.imencode('.jpg', frame)
    imageUpdateHelper(compressed_result)

    time.sleep(0.02)

cap.release()
