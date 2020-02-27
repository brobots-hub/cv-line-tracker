import cv2

def sub_contours(img_origin, y_from, y_to):
    y_from, y_to = max(1,int(y_from)), int(y_to)
    img = img_origin[-y_to:-y_from,:]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, 200, 255, 0)
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

def track(img, steps=10, y_limit=0.8, debug=False):
    result = []
    step_y = img.shape[0] * y_limit / steps
    nearest_x = img.shape[1] * 0.5
    for i in range(0,steps):
        cnts = sub_contours(img, i*step_y, (i+1)*step_y)
        if debug:
            cv2.drawContours(img, cnts, -1, (0,255,0), 3)
        tracks = []
        for j, cnt in enumerate(cnts):
            try:
                x,y = center(cnt)
                tracks.append((x,y))
                if debug:
                    cv2.circle(img, (x,y), 3, (255,0,0), 3)
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
                cv2.circle(img, (x,y), 3, (0,0,255), 3)
    return result


