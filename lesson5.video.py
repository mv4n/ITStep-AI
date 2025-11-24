# ВІДЕО
# import cv2
#
# img1 = cv2.imread('data/lesson3/sonet.png')
# img2 = cv2.imread('data/lesson3/sudoku.jpg')
#
#
# cv2.imshow('orig', img1)
#
# cv2.imshow('orig', img2)
#
#
# cv2.waitKey(0)

#
# import cv2
# from Tools.scripts.generate_opcode_h import write_int_array_from_ops
#
# # відкрити відео
# cap = cv2.VideoCapture(
#     0  # шлях до файлу або 0 для камери в ноутбуці
# )
#
# # інформація про відео
# # розмір кадрів
# print(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))) # Ширина
# print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) # Висота
# # FPS -- кількість кадрів у секунду
# print(int(cap.get(cv2.CAP_PROP_FPS)))
#
# # збереження відео
# # кодек(розширення файлу(mp4, avi, xvd))
# fourcc = cv2.VideoWriter_fourcc(*"mp4v")
#
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = int(cap.get(cv2.CAP_PROP_FPS))
#
# writer = cv2.VideoWriter(
#     'result.mp4', # шлях до файлу
#     fourcc, # кодек
#     fps,
#     (width, height)
# )
#
#
#
#
#
# # показ відео
# while True:
#     # дістати наступний кадр
#     success, img = cap.read()
#
#     # success -- True/False чи вдалось отримати кадр
#     if not success:
#         break # щось сталось, зупиняємо показ кадрів
#
#     # обробка кадру
#
#     # перевести зображення в чорно біле
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
#     # розмиття
#     gauss = cv2.GaussianBlur(
#         gray,
#         ksize=(9,9),
#         sigmaX=1
#     )
#
#     # бінарізація
#     adapt = cv2.adaptiveThreshold(
#         gauss,
#         255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         11,
#         2
#     )
#
#
#     cv2.imshow('original', img)
#     cv2.imshow('gray', gray)
#     cv2.imshow('gauss', gauss)
#     cv2.imshow('adapt', adapt)
#
#     # зберегти кадр до файлу
#     writer.write(img)
#
#
#     # чекаємо поки натиснеться кнопка на клавіатурі, але максимум 1 м/с
#
#     # якщо натиснута кнопка q то зупинити відео
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # отримати перший кадр
# _, img = cap.read()
# cv2.imshow('first frame', img)
# cv2.waitKey(0)
#
#
# # в кінці все закрити
# cap.release()
# writer.release()



# Пратика
# Завдання 3
# Відкрийте відео з файлу data\lesson7shapes.mp4. Проведіть виділення країв на кадрах та збережіть в новий файл.
import cv2


cap = cv2.VideoCapture('data/lesson7/shapes.mp4')

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(width * 0.5))
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(height * 0.5))

writer = cv2.VideoWriter(
    'bitwise.mp4',  # шлях до файлу
    fourcc,        # кодек
    fps,
    (width // 2, height // 2),
    isColor=False   # чи кадри кольорові
)


while True:
    success, img = cap.read()

    if not success:
        break

    img = cv2.resize(img, None, fx=0.5, fy=0.5)

    # hcv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # # 260 - 280 (130 - 140)
    # lower = (127, 40, 100)
    # upper = (150, 255, 255)
    #
    # res = cv2.inRange(hcv, lower, upper)

    hcv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = (0, 40, 100)
    upper = (20, 255, 255)
    #340 360(170 180)

    lower1 = (170, 40, 100)
    upper1 = (180, 255, 255)

    res = cv2.inRange(hcv, lower, upper)
    res2 = cv2.inRange(hcv, lower1, upper1)
    bitwise = cv2.bitwise_or(res, res2)

    cv2.imshow('orig', img)
    cv2.imshow('res', res2)
    cv2.imshow('bitwise', bitwise)

    writer.write(bitwise)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


cap.release()
writer.release()