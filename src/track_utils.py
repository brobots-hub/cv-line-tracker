import cv2
import numpy as np
import glob

cv2.namedWindow("img_path", cv2.WINDOW_KEEPRATIO )


def filter_color(img):
    img = cv2.bilateralFilter(img,9,75,75)
    lower_bound = np.array([30, 30, 30]) 
    upper_bound = np.array([150, 150,150]) 
    
    mask = cv2.inRange(img, lower_bound, upper_bound) 

    result = cv2.bitwise_and(img, img, mask=mask)
    return result




def filter_contours(contours, step):
    filtered = []
    for contour in contours:
        l = cv2.arcLength(contour, True)
        cnt_area = int(cv2.contourArea(contour))
        if cnt_area > 200*(10/step) and cnt_area < 10000*(10/step):
            filtered.append(contour)
    return filtered

def sub_contours(img_origin, y_from, y_to):
    y_from, y_to = max(1,int(y_from)), int(y_to)
    img = img_origin[-y_to:-y_from,:]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY_INV)
    thresh = cv2.bitwise_not(thresh)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        c += (0, img_origin.shape[0] - y_to)
    return contours

def center(cnt):
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return (int(cx), int(cy))

def track(img_origin, steps=10, y_limit=0.8, debug=False):
    result = []
    step_y = img_origin.shape[0] * y_limit / steps
    nearest_x = img_origin.shape[1] * 0.5
    img = filter_color(img)
    for i in range(0,steps):
        cnts = sub_contours(img, i * step_y, (i + 1) * step_y)
        cnts = filter_contours(cnts, steps)
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
            good_contours.append(cnts[min_index])
        if len(good_contours) >0 :
            cv2.drawContours(img_origin, good_contours, -1, (255, 0,0 ))

    
    return result


