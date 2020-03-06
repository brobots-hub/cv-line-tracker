import cv2
import numpy as np
import math
import time



def filter_color(img):
    img = cv2.bilateralFilter(img,9,75,75)
    lower_bound = np.array([100, 100, 100]) 
    upper_bound = np.array([255, 255,255]) 
    
    mask = cv2.inRange(img, lower_bound, upper_bound) 

    result = cv2.bitwise_and(img, img, mask=mask)
    return result

def filter_contours(img,contours, step):
    filtered = []
    for contour in contours:
        _,_,w,_ = cv2.boundingRect(contour)
        cnt_area = int(cv2.contourArea(contour))
        if cnt_area > 300:
            filtered.append(contour)
    return filtered


def sub_contours(img_origin, y_from, y_to, buff):
    y_from, y_to = max(1, int(y_from)), int(y_to)
    img = img_origin[-y_to:-y_from,:]
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.bilateralFilter(img,9,75,75)
    ret, thresh = cv2.threshold(img, 60, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    th = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
    thresh = cv2.bitwise_not(thresh)
    cv2.imshow("video2", thresh)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        c += (0, img_origin.shape[0] - y_to)
    return contours

def center(cnt):
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00']) 
    cy = int(M['m01']/M['m00'])
    return (int(cx), int(cy))

def track(img_origin, steps=10, y_limit=0.8, debug=False, buff=2):
    result = []
    step_y = img_origin.shape[0] * y_limit / steps
    nearest_x = img_origin.shape[1] * 0.5
    img = filter_color(img_origin)
    tt = time.time()
    for i in range(0, steps):
        cnts = sub_contours(img_origin, i * step_y, (i + 1) * step_y, buff)
        tracks = []
        good_contours = [] 

        for j, cnt in enumerate(cnts):
            try:
                x,y = center(cnt)
                tracks.append((x,y))


            except ZeroDivisionError:
                # bad contour
                pass
        if len(tracks) > 0:
            min_x = abs(nearest_x - tracks[0][0])
            min_index = 0
            for ind, track in enumerate(tracks):
                if abs(nearest_x - track[0]) < min_x:
                    min_x = abs(nearest_x - track[0]) 
                    min_index = ind
            x, y = tracks[min_index]
            result.append((x,y))
            nearest_x = x
            if debug:
                cv2.circle(img_origin, (x, y), 3, (0, 0, 255), 2)
    distances = []
    print(time.time() - tt)

    for i in range(len(result)):
        try:
            if abs(result[i][0] - result[i+1][0]) < img_origin.shape[1]*0.3 :
                cv2.line(img_origin, result[i], result[i + 1], (255, 255, 0), 5)
                try:
                    if (result[i][0] * 0.0008125) > 0.1 and (result[i][0] * 0.0008125) < 0.2:
                        distances.append(round(result[i][0] * 0.0008125, 2))
                except:
                    pass


            else:
                break
        except:
            pass
    return distances