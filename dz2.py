import cv2
import numpy as np
# Завдання 1
# img = cv2.imread("data/lesson1/Lenna.png")
#
# mask1 = cv2.imread("data/lesson1/mask1.png", cv2.IMREAD_GRAYSCALE)
# mask2 = cv2.imread("data/lesson1/mask2.png", cv2.IMREAD_GRAYSCALE)
#
# mask1 = mask1 > 0
# mask2 = mask2 > 0
#
# mask_or = cv2.bitwise_or(mask1.astype(np.uint8), mask2.astype(np.uint8)).astype(bool)
#
# res1 = img.copy()
# res1[~mask1] = 0
#
# res2 = img.copy()
# res2[~mask2] = 0
#
# res_or = img.copy()
# res_or[~mask_or] = 0
#
# cv2.imshow("Original", img)
# cv2.imshow("Mask1 result", res1)
# cv2.imshow("Mask2 result", res2)
# cv2.imshow("Mask1 OR Mask2", res_or)
#
# cv2.waitKey(0)

# Завдання 2

img = cv2.imread("data/lesson1/baboo.jpg", cv2.IMREAD_GRAYSCALE)

cut_img = img[0:50, 50:200]
cv2.imshow('cut', cut_img)

cv2.waitKey(0)
