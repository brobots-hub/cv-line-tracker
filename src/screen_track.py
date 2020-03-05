from Xlib import display, X
from PIL import Image
import numpy
import cv2
import src.track_utils as track_utils

root_window = display.Display().screen().root
y_limit_bottom = 0.9

def xlib_to_cv2(root):
    geom = root.get_geometry()
    height = int(geom.height * y_limit_bottom)
    data = root.get_image(0,0, geom.width, height, X.ZPixmap, 0xffffffff).data
    image = Image.frombytes("RGB", (geom.width, height), data, "raw", "BGRX")
    return numpy.array(image.convert('RGB'))

def display_test(name='test'):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 800, 600)
    cv2.imshow(name, xlib_to_cv2(root_window))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def loop():
    name = 'test'
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(name, 400, 250)
    thresh1 = 0
    thresh2 = 255
    try:
        while True:
            key = cv2.waitKey(20)
            if key > 0:
                if key == ord('q'):
                    break
                elif key == ord('w'):
                    thresh1 = min(255, thresh1+10)
                elif key == ord('s'):
                    thresh1 = max(0, thresh1-10)
                elif key == ord('e'):
                    thresh2 = min(255, thresh2+10)
                elif key == ord('d'):
                    thresh2 = max(0, thresh2-10)
            img = xlib_to_cv2(root_window)
            track_utils.track(img, steps=30, y_limit = 0.7, debug=True)
            #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #ret, thresh = cv2.threshold(img, thresh1, thresh2, 0)
            #thresh = cv2.bitwise_not(thresh)
            cv2.imshow(name, img)
    finally:
        print(thresh1, thresh2)
        cv2.destroyAllWindows()
