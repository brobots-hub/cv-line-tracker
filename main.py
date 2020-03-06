import glob
import cv2
import src.track_utils as track_utils
import sys
import requests
import time
cap = cv2.VideoCapture('http://'+ sys.argv[1] +':8088/stream/video.mjpeg')
cv2.namedWindow("video", cv2.WINDOW_NORMAL)
cv2.namedWindow("video2", cv2.WINDOW_NORMAL)
alpha_slider_max = 100
title_window = 'Linear Blend'
skip_counter = 0
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1);
while (cap.isOpened()):
    if skip_counter%2400 == 0:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        a = track_utils.track(frame, steps=20, y_limit=1, debug=True)
        if len(a) >0:
            r = requests.post(url="http://" + sys.argv[1] + ":8080/api/v1/servo", data={"angle": a[1]})
            #r = requests.post(url="http://" + sys.argv[1] + ":8080/api/v1/motor", data={"power": 0.2})
            #time.sleep(0.1)
            #r = requests.post(url="http://" + sys.argv[1] + ":8080/api/v1/motor", data={"power": 0.0})
            #print(a[0])
        cv2.imshow("video",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    skip_counter+=1
cap.release()
cv2.destroyAllWindows()

