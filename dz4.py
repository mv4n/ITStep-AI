# import cv2
# import numpy as np
#
# img = cv2.imread('data/lesson3/sonet.png', cv2.IMREAD_GRAYSCALE)
#
# gaus = cv2.GaussianBlur(
#     img,
#     (5, 5),
#     2
# )
#
# bilateral = cv2.bilateralFilter(
#     gaus,
#     d=7,
#     sigmaColor=75,
#     sigmaSpace=75
# )
#
# bin_adapt = cv2.adaptiveThreshold(
#     bilateral,
#     255,
#     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#     cv2.THRESH_BINARY,
#     11,
#     2
# )
#
# cv2.imshow('orig', img)
# cv2.imshow('res', bin_adapt)
# cv2.waitKey(0)




import cv2
import numpy as np

img_n = cv2.imread('data/lesson3/sonet_noised.png', cv2.IMREAD_GRAYSCALE)

gaus_n = cv2.GaussianBlur(
    img_n,
    (3, 3),
    11
)

bilateral_n = cv2.bilateralFilter(
    gaus_n,
    d=3,
    sigmaColor=75,
    sigmaSpace=75
)

bin2 = cv2.adaptiveThreshold(
    bilateral_n,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    15,
    2
)

cv2.imshow('orig', img_n)
cv2.imshow('res', bin2)
cv2.waitKey(0)


