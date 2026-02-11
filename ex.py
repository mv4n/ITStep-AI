import cv2
import mediapipe as mp
import math
import time
import win32com.client
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Конфігурація для детекції жестів
class DetectionSettings:
    def __init__(self):
        self.z_variance_limit = 0.055
        self.finger_bend_limit = 18
        self.thumb_left_limit = 0.11
        self.thumb_right_limit = -0.11
        self.thumb_vertical_limit = 0.16

config = DetectionSettings()

# З'єднання з PowerPoint
pp_app = win32com.client.Dispatch("PowerPoint.Application")
pp_app.Visible = True
deck = pp_app.Presentations.Open(r"C:\users\shapa\downloads\example.pptx")
deck_window = deck.Windows(1)

def flip_forward():
    slide_num = deck_window.View.Slide.SlideIndex
    if slide_num < deck.Slides.Count:
        deck_window.View.GotoSlide(slide_num + 1)

def flip_backward():
    slide_num = deck_window.View.Slide.SlideIndex
    if slide_num > 1:
        deck_window.View.GotoSlide(slide_num - 1)

# Функція для розрахунку кута
def get_angle_between_points(pt1, pt2, pt3):
    dir1 = (pt2.x - pt1.x, pt2.y - pt1.y, pt2.z - pt1.z)
    dir2 = (pt2.x - pt3.x, pt2.y - pt3.y, pt2.z - pt3.z)
    scalar_prod = sum(x * y for x, y in zip(dir1, dir2))
    len_dir1 = math.sqrt(sum(z**2 for z in dir1))
    len_dir2 = math.sqrt(sum(z**2 for z in dir2))
    if len_dir1 * len_dir2 == 0:
        return 180
    cos_angle = scalar_prod / (len_dir1 * len_dir2)
    return math.degrees(math.acos(cos_angle))

# Ініціалізація моделі ШІ
load_dotenv()
gemini_token = os.getenv("GEMINI_API_KEY")
ai_generator = GoogleGenerativeAI(model="gemini-2.5-flash", api_key=gemini_token)

content_prompt = PromptTemplate.from_template(
    """Генеруй корисний контент для слайда на основі заголовка.
Заголовок: {header}"""
)
content_flow = content_prompt | ai_generator

# Налаштування для розпізнавання рук
hand_mp = mp.solutions.hands
draw_mp = mp.solutions.drawing_utils
webcam = cv2.VideoCapture(0)

detection_delay = 1.2
detection_start = None
content_creating = False

with hand_mp.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as detector:

    while True:
        grabbed, img = webcam.read()
        if not grabbed:
            break

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        detection_output = detector.process(img_rgb)

        if detection_output.multi_hand_landmarks:
            for marks, side_info in zip(detection_output.multi_hand_landmarks, detection_output.multi_handedness):
                draw_mp.draw_landmarks(img, marks, hand_mp.HAND_CONNECTIONS)
                hand_orientation = side_info.classification[0].label
                if hand_orientation == "Right":
                    continue

                # Точки на руці
                big_tip = marks.landmark[4]
                big_base = marks.landmark[2]
                ptr_tip = marks.landmark[8]
                ptr_base = marks.landmark[5]
                ptr_joint1 = marks.landmark[6]
                ptr_joint2 = marks.landmark[7]
                mid_tip = marks.landmark[12]
                mid_base = marks.landmark[9]
                mid_joint1 = marks.landmark[10]
                mid_joint2 = marks.landmark[11]
                rng_tip = marks.landmark[16]
                rng_base = marks.landmark[13]
                rng_joint1 = marks.landmark[14]
                rng_joint2 = marks.landmark[15]
                lit_tip = marks.landmark[20]
                lit_base = marks.landmark[17]
                lit_joint1 = marks.landmark[18]
                lit_joint2 = marks.landmark[19]

                # Логіка детекції
                curled_left = (
                    ptr_tip.y > ptr_base.y + 0.015 and
                    mid_tip.y > mid_base.y + 0.015 and
                    rng_tip.y > rng_base.y + 0.015 and
                    lit_tip.y > lit_base.y + 0.015
                )
                curled_right = (
                    ptr_tip.y < ptr_base.y - 0.015 and
                    mid_tip.y < mid_base.y - 0.015 and
                    rng_tip.y < rng_base.y - 0.015 and
                    lit_tip.y < lit_base.y - 0.015
                )

                mean_z = sum([big_tip.z, ptr_tip.z, mid_tip.z, rng_tip.z, lit_tip.z]) / 5
                level_fingers = all(abs(mark.z - mean_z) < config.z_variance_limit
                                    for mark in [big_tip, ptr_tip, mid_tip, rng_tip, lit_tip])

                bends_ok = (
                    get_angle_between_points(ptr_joint2, ptr_joint1, ptr_base) < config.finger_bend_limit and
                    get_angle_between_points(mid_joint2, mid_joint1, mid_base) < config.finger_bend_limit and
                    get_angle_between_points(rng_joint2, rng_joint1, rng_base) < config.finger_bend_limit and
                    get_angle_between_points(lit_joint2, lit_joint1, lit_base) < config.finger_bend_limit
                )

                big_left = big_tip.x - big_base.x > config.thumb_left_limit
                big_right = big_tip.x - big_base.x < config.thumb_right_limit
                big_side_l = big_tip.x > max(ptr_base.x, lit_base.x)
                big_side_r = big_tip.x < min(ptr_base.x, lit_base.x)
                big_upward = (big_tip.y - big_base.y) < config.thumb_vertical_limit

                swipe_l = curled_left and level_fingers and big_left and big_side_l and bends_ok
                swipe_r = curled_right and level_fingers and big_right and big_side_r and bends_ok
                big_up = big_upward and bends_ok

                current_t = time.time()

                if swipe_l or swipe_r or big_up:
                    if content_creating:
                        detection_start = None
                        continue
                    if detection_start is None:
                        detection_start = current_t
                    elif current_t - detection_start >= detection_delay:
                        if swipe_l:
                            flip_backward()
                            print("Свайп ліворуч — назад")
                        elif swipe_r:
                            flip_forward()
                            print("Свайп праворуч — вперед")
                        else:
                            curr_slide = deck_window.View.Slide
                            slide_head = curr_slide.Shapes.Title.TextFrame.TextRange.Text
                            content_creating = True
                            new_content = content_flow.invoke({"header": slide_head})
                            curr_slide.Shapes.Placeholders(2).TextFrame.TextRange.Text = new_content
                            content_creating = False
                            deck.Save()
                            print("Великий палець вгору — контент додано")
                        detection_start = None
                else:
                    detection_start = None

        cv2.imshow("Потік з вебкамери", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

webcam.release()
deck.Close()
pp_app.Quit()
cv2.destroyAllWindows()