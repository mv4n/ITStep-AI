import numpy as np
import ultralytics
import cv2

from lesson6 import success

# модель для сегментації
model = ultralytics.YOLO('yolo11s-seg.pt')

# img = cv2.imread('data/lesson_seg/human.jpg')
#
# # застосування моделі
# # results -- list з результатами для кожного зоображення в predict
# results = model.predict(
#     img,
#     conf=0.5
# )
#
# # дістати результати для першого(єдиного) зоображення
# result = results[0]
#
# # візуалізація результату
# res_img = result.plot(
#     boxes=True, # чи показувати рамки
#     masks=True   # чи показувати маски сегментації
# )
#
# # маски об'єктів
# masks = result.masks
#
# # класи обєктів
# names = result.names
#
# # де знаходиться людина
# idx = 0
# # маска людини
# mask = masks[idx]
#
# # переведення маски у формат opencv
# mask = mask.cpu() # відключення від графічного процесора
# mask = mask.numpy() # переведення у масив numpy
# mask = mask.astype(np.uint8) # зміна типу даних
#


# Відео
cap = cv2.VideoCapture(0)

# зоображення фону
background_img = cv2.imread('data/lesson4/canal.png')

# зміна розміру зображення з фоном


while True:
    success, img = cap.read()

    if not success:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # застосувати модель

    results = model.predict(img)
    result = results[0]

    res_img = result.plot()

    # маска
    masks = result.masks.data
    mask = masks[0]
    mask = mask.cpu()
    mask = mask.numpy()
    mask = mask.astype(np.uint8)
    mask *= 255

    mask_bool = mask.astype(bool)

    # заміна пікселів які не людина
    img[~mask_bool] = background_img


    cv2.imshow('mask', mask)
    cv2.imshow('res', res_img)
    cv2.imshow('orig', img)

#
# cv2.imshow('result', res_img)
# cv2.imshow('orig', img)
cv2.waitKey(0)