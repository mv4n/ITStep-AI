# import ultralytics
# import cv2
#
# model = ultralytics.YOLO('yolov8s.pt')
#
# cap = cv2.VideoCapture('data/lesson8/meetings.mp4')
#
# while True:
#     success, frame = cap.read()
#     if not success:
#         break
#
#     frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
#
#     results = model.predict(frame, device='cpu', conf=0.25, iou=0.7)
#     result = results[0]
#
#     res_img = result.plot()
#     cv2.imshow('Task 1 - People Detection', res_img)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cv2.waitKey(0)

import ultralytics
import cv2
import numpy as np

model = ultralytics.YOLO('yolov8s.pt')

cap = cv2.VideoCapture('data/lesson8/meetings.mp4')

start_showing = False

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)

    results = model.predict(frame, device='cpu', conf=0.25, iou=0.7)
    result = results[0]

    cls_ids = result.boxes.cls.cpu().numpy()
    num_people = np.sum(cls_ids == 0)

    if num_people >= 5:
        start_showing = True

    if start_showing:
        res_img = result.plot()
        cv2.imshow('people', res_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
