import cv2

img = cv2.imread('./data/track-photo/IMG_3825.JPG')

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
