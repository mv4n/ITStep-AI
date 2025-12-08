# детекція обєктів(YOLO)

import ultralytics
import cv2

# створення моделі
model = ultralytics.YOLO('yolov8s.pt')

# отримати зображення з відео
cap = cv2.VideoCapture('data/lesson8/cars+bikes.mp4')
success, img = cap.read()

img = cv2.resize(img, None, fx=0.5, fy=0.5)

cv2.imshow('original', img)


# застосування моделі
# predict може отримувати декілька зобржанеь за раз
# predict([img1, img2, img3]) і тому results це списко
# [result1, result2, result3]
results = model.predict(
    img, # саме зоображення
    device='cpu', # процесор де запускати модель
                  # cpu -- звичайний процес
                  # cuda -- графічний процесор
    conf = 0.25,  # мінімальний відсоток для обєкта щоб попасти в result
    iou=0.7       # максимально можливий рівень перетину рамок(якщо більше то вважаємо
                  # що це рамки для одного й того самого обєкта)
)
# results -- список з одним елементом
result = results[0]

# отримати назви класів(обєкти які вміє визначати модель)
names = result.names # dict --- id: str




# самі обєкти
cls = result.boxes.cls
print(cls)

# візуалізація результатів
res_img = result.plot()
cv2.imshow('result', res_img)



# ймовірності
conf = result.boxes.conf
print(conf)

# рамка(box)
boxes = result.boxes

# отримати перший обєкт
box = boxes[0]
print(box)

# координати
xyxy = box.xyxy[0]

# переведення координат в int
x1, y1, x2, y2 = map(int, xyxy)

# вирізати обєкт з всього зоображення
# y -- відповідають за рядки
# x -- відповідають за стопчики
roi = img[y1:y2, x1:x2]

cv2.imshow('object', roi)

# відео
# while True:
#     success, img = cap.read()
#
#     if not success:
#         break
#
#     img = cv2.resize(img, None, fx=0.5, fy=0.5)
#
#     results = model.predict(img)
#     result = results[0]
#
#     res_img = result.plot()
#
#     cv2.imshow('result', res_img)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

cv2.waitKey(0)