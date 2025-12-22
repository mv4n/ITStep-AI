import cv2

cap = cv2.VideoCapture('data/lesson7/meter.mp4')


fourcc = cv2.VideoWriter_fourcc(*"mp4v")
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Відео збережемо в чорно-білому форматі
writer = cv2.VideoWriter(
    'meter_binary.mp4',
    fourcc,
    fps,
    (width, height),
    isColor=False
)

while True:
    success, img = cap.read()
    if not success:
        break

    filtered = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

    binary = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    cv2.imshow('Original', img)
    cv2.imshow('Binary', binary)

    writer.write(binary)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
writer.release()
