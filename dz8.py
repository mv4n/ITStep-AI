import cv2
import ultralytics
import numpy as np
import math

def get_angle(x1, y1, x2, y2, x3, y3):
    a = (x1 - x2, y1 - y2)
    b = (x3 - x2, y3 - y2)
    dot = a[0]*b[0] + a[1]*b[1]
    mag_a = math.sqrt(a[0]**2 + a[1]**2)
    mag_b = math.sqrt(b[0]**2 + b[1]**2)
    return math.degrees(math.acos(dot / (mag_a * mag_b)))

model = ultralytics.YOLO("yolo11s-pose.pt")
cap = cv2.VideoCapture("data/lesson_pose/squat.mp4")

counter = 0
state = "UP"

ANGLE_DOWN = 90
ANGLE_UP = 160


def get_max_index(result):
    boxes = result.boxes.xywh
    area = (boxes[:, 2] * boxes[:, 3]).cpu().numpy()
    return np.argmax(area)


while True:
    success, img = cap.read()
    if not success:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    results = model.predict(img, verbose=False)
    result = results[0]

    if result.boxes is None:
        continue

    idx = get_max_index(result)
    keypoints = result.keypoints[idx].xy[0]

    hip = keypoints[11]
    knee = keypoints[13]
    ankle = keypoints[15]

    x1, y1 = int(hip[0]), int(hip[1])
    x2, y2 = int(knee[0]), int(knee[1])
    x3, y3 = int(ankle[0]), int(ankle[1])

    angle = get_angle(x1, y1, x2, y2, x3, y3)

    if angle < ANGLE_DOWN and state == "UP":
        state = "DOWN"

    if angle > ANGLE_UP and state == "DOWN":
        counter += 1
        state = "UP"

    cv2.putText(img, f"Angle: {int(angle)}",
                (x2 - 40, y2 - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.putText(img, f"Squats: {counter}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.circle(img, (x1, y1), 5, (255, 0, 0), -1)
    cv2.circle(img, (x2, y2), 5, (0, 255, 0), -1)
    cv2.circle(img, (x3, y3), 5, (255, 0, 0), -1)

    cv2.imshow("Squat Angle Counter", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.waitKey(0)
