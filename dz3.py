import cv2
import numpy as np

img = cv2.imread('data/lesson2/darken.png')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

h, s, v = cv2.split(hsv)
v_eq = cv2.equalizeHist(v)
hsv_eq = cv2.merge([h, s, v_eq])
res_eq = cv2.cvtColor(hsv_eq, cv2.COLOR_HSV2BGR)

v_float = v.astype(np.float32)
v_inc = v_float * 1.3   # +30%

v_inc = np.clip(v_inc, 0, 255)
v_inc = v_inc.astype(np.uint8)

hsv_inc = cv2.merge([h, s, v_inc])
res = cv2.cvtColor(hsv_inc, cv2.COLOR_HSV2BGR)

cv2.imshow('Orig', img)
cv2.imshow('Histogram', res_eq)
cv2.imshow('res', res)

cv2.waitKey(0)
cv2.destroyAllWindows()
