import cv2
import numpy as np
import matplotlib.pyplot as plt
import functools


def trackbar_decorator(**kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            window_name = func.__name__
            cv2.namedWindow(window_name)

            trackbar_values = {}

            for param, (min_val, max_val) in kwargs.items():
                cv2.createTrackbar(param, window_name, min_val, max_val, lambda x: None)
                trackbar_values[param] = min_val

            while True:
                for param in kwargs:
                    trackbar_values[param] = cv2.getTrackbarPos(param, window_name)

                result = func(*args, **trackbar_values)
                cv2.imshow(func.__name__, result)

                if cv2.waitKey(1) & 0xFF == 27:
                    break

            cv2.destroyAllWindows()
            return result

        return wrapper

    return decorator


def add_gaussian_noise(image, mean=0, std=25):
    noise = np.random.normal(mean, std, image.shape).astype(np.int8)
    image = image + noise
    noisy_image = np.clip(image, 0, 255).astype(np.uint8)  # Ensures pixel values remain valid
    return noisy_image


def add_salt_and_pepper_noise(image, salt_prob=0.002, pepper_prob=0.002):
    noisy_image = image.copy()
    total_pixels = image.size

    # Adding salt (white pixels)
    num_salt = int(total_pixels * salt_prob)
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape[:2]]
    noisy_image[coords[0], coords[1]] = 255  # White pixels

    # Adding pepper (black pixels)
    num_pepper = int(total_pixels * pepper_prob)
    coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape[:2]]
    noisy_image[coords[0], coords[1]] = 0  # Black pixels

    return noisy_image


def add_poisson_noise(image):
    noise = np.random.poisson(image.astype(np.float32))  # Poisson noise
    noisy_image = np.clip(noise, 0, 255).astype(np.uint8)
    return noisy_image


def add_speckle_noise(image, mean=0, std=0.1):
    noise = np.random.normal(mean, std, image.shape)
    noisy_image = image + image * noise
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return noisy_image


@trackbar_decorator(value=(0, 255))
def lesson1_image(value):
    img = np.full((400, 400), value, dtype=np.uint8)
    return img


@trackbar_decorator(b=(0, 255), g=(0, 255), r=(0, 255))
def lesson2_bgr_range(b, g, r):
    img = np.empty((400, 400, 3), dtype=np.uint8)

    img[:, :, 0] = b
    img[:, :, 1] = g
    img[:, :, 2] = r

    return img


@trackbar_decorator(hue=(0, 180), sat=(255, 255), val=(255, 255))
def lesson2_hsv_range(hue, sat, val):
    hsv = np.empty((400, 400, 3), dtype=np.uint8)

    hsv[:, :, 0] = hue
    hsv[:, :, 1] = sat
    hsv[:, :, 2] = val

    img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img


@trackbar_decorator(l=(0, 255), a=(0, 255), b=(0, 255))
def lesson2_lab_range(l, a, b):
    lab = np.empty((400, 400, 3), dtype=np.uint8)

    lab[:, :, 0] = l
    lab[:, :, 1] = a
    lab[:, :, 2] = b

    img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return img


def lesson3_plot_hist(img):
    hist = cv2.calcHist([img], [0], None, [256], [0, 256])
    plt.plot(hist)
    plt.show()


@trackbar_decorator(ksize=(2, 21), sigma=(0, 10))
def lesson3_gaussian(img, ksize, sigma):
    if sigma % 2 == 0:
        sigma += 1

    return cv2.GaussianBlur(img, (ksize, ksize), sigma)


@trackbar_decorator(ksize=(2, 21))
def lesson3_median(img, ksize, sigma):
    if sigma % 2 == 0:
        sigma += 1

    return cv2.medianBlur(img, ksize)


@trackbar_decorator(h=(1, 21), templateWindowSize=(2, 21), searchWindowSize=(2, 41))
def lesson3_NLMean(img, h, templateWindowSize, searchWindowSize):
    if templateWindowSize % 2 == 0:
        templateWindowSize += 1

    if searchWindowSize % 2 == 0:
        searchWindowSize += 1

    return cv2.fastNlMeansDenoising(img, h, templateWindowSize, searchWindowSize)


@trackbar_decorator(d=(1, 100), sigmaColor=(1, 150), sigmaSpace=(1, 150))
def lesson3_bilateral(image, d, sigmaColor, sigmaSpace):
    return cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)


def show_cards(img, cnts):
    for i, cnt in enumerate(cnts, start=1):
        # знаходимо краї контуру
        bottom_left = np.argmin(cnt[:, 0, 0] - cnt[:, 0, 1])
        top_right = np.argmax(cnt[:, 0, 0] - cnt[:, 0, 1])
        top_left = np.argmin(cnt[:, 0, 0] + cnt[:, 0, 1])
        bottom_right = np.argmax(cnt[:, 0, 0] + cnt[:, 0, 1])

        pt1 = cnt[bottom_left, 0]
        pt2 = cnt[top_right, 0]
        pt3 = cnt[top_left, 0]
        pt4 = cnt[bottom_right, 0]

        # різмір зображення для однієї карти
        w, h = 200, 300


        # матриця перетворень
        H = cv2.getPerspectiveTransform(
            np.array([pt3, pt2, pt1, pt4], dtype=np.float32),
            np.array([[0, 0], [w-1, 0], [0, h-1], [w-1, h-1]], dtype=np.float32),
        )

        # дістаємо потрібну область
        roi = cv2.warpPerspective(img, H, dsize=(w, h))

        cv2.imshow(f'card {i}', roi)


import numpy as np

def get_angle(x1, y1, x2, y2, x3, y3):
    a = np.array([x1, y1])
    b = np.array([x2, y2])
    c = np.array([x3, y3])

    ab = a - b
    cb = c - b

    dot = ab @ cb
    norm_ab = (ab @ ab) ** 0.5
    norm_cb = (cb @ cb) ** 0.5
    angle = np.arccos(dot / norm_ab / norm_cb)
    angle = angle / np.pi * 180

    return angle