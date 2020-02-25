import glob

import cv2
import src.track_utils as track_utils

for img_path in glob.glob('./data/track-photo/*.JPG'):
    img = cv2.imread(img_path)
    print(track_utils.track(img, steps=30, y_limit=0.7, debug=True))

    cv2.namedWindow(img_path, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(img_path, 800, 600)

    cv2.imshow(img_path, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
