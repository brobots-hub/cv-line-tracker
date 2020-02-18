import cv2
import numpy as np
import math


def filter_color(img):
    img = cv2.bilateralFilter(img,9,75,75)
    lower_bound = np.array([100, 100, 100]) 
    upper_bound = np.array([255, 255,255]) 
    
    mask = cv2.inRange(img, lower_bound, upper_bound) 

    result = cv2.bitwise_and(img, img, mask=mask)
    return result

def find_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return round(ang + 360) if ang < 0 else round(ang)




def filter_contours(img,contours, step):
    filtered = []
    for contour in contours:
        _,_,w,_ = cv2.boundingRect(contour)
        cnt_area = int(cv2.contourArea(contour))
        if cnt_area > ((img.shape[0] * img.shape[1]) * 0.10 / step) and (cnt_area < ((img.shape[0] * img.shape[1]) * 0.7) / step) and w < (img.shape[1]*0.5):
            filtered.append(contour)
    return filtered


def sub_contours(img_origin, y_from, y_to):
    y_from, y_to = max(1,int(y_from)), int(y_to)
    img = img_origin[-y_to:-y_from,:]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, 127, 255, 0)
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
    img = filter_color(img_origin)

    for i in range(0,steps):
        cnts = sub_contours(img, i * step_y, (i+1)* step_y)
        cnts = filter_contours(img,cnts, steps)
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
    angles = []
    for i in range(len(result)):
        try:
            if abs(result[i+1][0] - result[i][0]) < img_origin.shape[1]*0.2 :
                cv2.line(img_origin, result[i], result[i + 1], (255, 255, 0), 5)
                try:
                    if len(angles) ==0:
                        angles.append(find_angle((result[i - 1][0], 0), (result[i - 1][0], result[i][1]), result[i + 1]))
                        angles.append(find_angle(result[i-1], result[i], result[i+1]))
                    else:
                        angles.append((angles[-1] - find_angle(result[i - 1], result[i], result[i + 1])))
                except:
                    pass


            else:
                break
        except:
            pass
    return angles



