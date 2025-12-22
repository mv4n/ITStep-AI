import cv2
import numpy as np

img = cv2.imread('data/lesson3/sonet.png', cv2.IMREAD_GRAYSCALE)

gaus = cv2.GaussianBlur(
    img,
    (5, 5),
    2
)

bilateral = cv2.bilateralFilter(
    gaus,
    d=7,
    sigmaColor=75,
    sigmaSpace=75
)

bin_adapt = cv2.adaptiveThreshold(
    bilateral,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)

cv2.imshow('orig', img)
cv2.imshow('res', bin_adapt)
cv2.waitKey(0)
cv2.destroyAllWindows()
