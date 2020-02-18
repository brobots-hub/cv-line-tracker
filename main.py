import glob
import cv2
import src.track_utils as track_utils

cap = cv2.VideoCapture('./data/track-photo/video_2020-02-10_14-31-54.mp4')
cv2.namedWindow("video", cv2.WINDOW_NORMAL)
i=0
while (cap.isOpened()):
    if i % 1000 == 0:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        print(track_utils.track(frame, steps=10, y_limit = 1, debug=True))
        cv2.imshow("video",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    i += 1;
cap.release()
cv2.destroyAllWindows()

