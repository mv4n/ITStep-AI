# згортка
# import cv2
from torch.ao.nn.quantized.functional import threshold

import utils
import numpy as np

# img = cv2.imread('data/lesson3/castello_noised.png')


# ядро згортки(фільтр, масив з коефіцієнтами)

# kernel = np.array(
#     [[-1, 0, 1],
#      [-2., 0., 2.],
#      [-1, 0, 1]]
# )
#
# res = cv2.filter2D(img, -1, kernel)
#
# cv2.imshow('kernel', res)




# застосування -- усунення шуму
# img = utils.add_salt_and_pepper_noise(img, 0.001, 0.001)

# гаусове розмиття
# res = cv2.GaussianBlur(
#     img,
#     (13,13), # розмір ядра
#     2
# )
#
# # двосторонній фільтр
# res = cv2.bilateralFilter(
#     img,
#     d=9, # розмір ядра
#     sigmaColor=75,
#     sigmaSpace=75, # те ж саме що й в GaussianBlur
# )
#
# cv2.imshow('result', res)



# бінарізація
# зоображення має бути чорно біле
# img = cv2.imread('data/lesson3/darken_page.jpg')
#
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


# проста бінарізація
# threshold = 5 # порогове значення
#
# res = gray.copy()
# mask = res > threshold
# gray[mask] = 255
# gray[~mask] = 0

# адаптивна бінарізація
# res = cv2.adaptiveThreshold(
#     gray,
#     255, # інтенсивність для білого кольору
#     cv2.ADAPTIVE_THRESH_MEAN_C, # формула згортки(гаус)
#     cv2.THRESH_BINARY, # це не чіпаємо
#     11, # розмір ядра для згортки
#     2 # наскільки чутливою має бути бінарізація
# )
#
# cv2.imshow('res', res)
# cv2.imshow('original', img)
# cv2.waitKey(0)

# Практичне завдання
# Завдання 1
# Відкрийте зображення data/lesson3/notes.png. Проведіть наступні дії:
#  проведіть бінарізацію(звичайну та адаптивну)
#  застосуйте розмиття(гаусове) візьміть ядра 3, 5, 11 та sigmaX 0, 2, 10
#  повторіть бінарізацію, але перед тим застосуйте bilateral filter
# import cv2
#
# img = cv2.imread('data/lesson3/notes.png', cv2.IMREAD_GRAYSCALE)

# звичайні(проста) бінарізація

# threshold = 100 # порогове значення
#
# res = img.copy()
# mask = res > threshold
# res[mask] = 255
# res[~mask] = 0
# cv2.imshow('res', res)


# адаптивна бінарізація
# res = cv2.adaptiveThreshold(
#     img,
#     255, # інтенсивність для білого кольору
#     cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # формула згортки(гаус)
#     cv2.THRESH_BINARY, # це не чіпаємо
#     11, # розмір ядра для згортки
#     4 # наскільки чутливою має бути бінарізація
# )
# cv2.imshow('res', res)



# гаусове розмиття

# res = cv2.GaussianBlur(
#     img,
#     (3,3), # розмір ядра
#     0
# )
# cv2.imshow('res1', res)
#
# res = cv2.GaussianBlur(
#     img,
#     (5,5), # розмір ядра
#     2
# )
# cv2.imshow('res2', res)

# res = cv2.GaussianBlur(
#     img,
#     (11,11), # розмір ядра
#     10
# )
# cv2.imshow('res3', res)


# повторіть бінарізацію, але перед тим застосуйте bilateral filter

# res = cv2.bilateralFilter(
#     img,
#     d=9, # розмір ядра
#     sigmaColor=75,
#     sigmaSpace=75, # те ж саме що й в GaussianBlur
# )
#
# cv2.imshow('result', res)
#
# res2 = cv2.adaptiveThreshold(
#     res,
#     255, # інтенсивність для білого кольору
#     cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # формула згортки(гаус)
#     cv2.THRESH_BINARY, # це не чіпаємо
#     11, # розмір ядра для згортки
#     2 # наскільки чутливою має бути бінарізація
# )
# cv2.imshow('res', res2)
#
# cv2.imshow('orig', img)

# Завдання 2
# Відкрийте зображення data/lesson3/sudoku.jpg. Проведіть для нього бінарізацію, а саме
#  CLAHE
#  гаусове розмиття
#  адаптивна бінарізація
#  NLMean
# Самостійно підберіть параметри, збережіть результат. Порівняйте результати для гаусової та середньої адаптивної бінарізації

import cv2

img = cv2.imread('data/lesson3/sudoku.jpg', cv2.IMREAD_GRAYSCALE)
res = cv2.GaussianBlur(
    img,
    (3,3), # розмір ядра
    2
)
cv2.imshow('GAUS', res)

res1 = cv2.adaptiveThreshold(
    img,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    2
)

cv2.imshow('adaptive_original', res1)

res2 = cv2.adaptiveThreshold(
    res,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    7,
    3
)

cv2.imshow('adaptive_gause', res2)


res3 = cv2.bilateralFilter(
    img,
    d=3, # розмір ядра
    sigmaColor=75,
    sigmaSpace=75, # те ж саме що й в GaussianBlur
)
cv2.imshow('bilateral', res3)

res4 = cv2.adaptiveThreshold(
    res3,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    5,
    4
)
cv2.imshow('bilateral_adaptive', res4)

cv2.imshow('orig', img)
cv2.waitKey(0)
