import cv2
import mediapipe as mp
import math
import time
import win32com.client
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os
import dotenv

# Клас порогів жестів
class GestureThresholds:
    def __init__(self):
        # Допустимі відхилення по Z координаті
        self.z_tolerance = 0.05
        # Максимальний кут фаланг пальців
        self.max_finger_angle = 20
        # Пороги для великого пальця
        self.thumb_left = 0.1
        self.thumb_right = -0.1
        self.thumb_up = 0.15

# Ініціалізація
thresholds = GestureThresholds()

# PowerPoint
ppt_app = win32com.client.Dispatch("PowerPoint.Application")
ppt_app.Visible = True
presentation = ppt_app.Presentations.Open(r"C:\users\shapa\downloads\example.pptx")
ppt_window = presentation.Windows(1)

def next_slide():
    idx = ppt_window.View.Slide.SlideIndex
    if idx < presentation.Slides.Count:
        ppt_window.View.GotoSlide(idx + 1)

def previous_slide():
    idx = ppt_window.View.Slide.SlideIndex
    if idx > 1:
        ppt_window.View.GotoSlide(idx - 1)

# Допоміжні функції
def calculate_angle(a, b, c):
    vec1 = (b.x - a.x, b.y - a.y, b.z - a.z)
    vec2 = (b.x - c.x, b.y - c.y, b.z - c.z)
    dot = sum(vec1[i] * vec2[i] for i in range(3))
    mag1 = math.sqrt(sum(x * x for x in vec1))
    mag2 = math.sqrt(sum(x * x for x in vec2))
    if mag1 * mag2 == 0:
        return 180
    return math.degrees(math.acos(dot / (mag1 * mag2)))

# Google Generative AI
dotenv.load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

ai_model = GoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=gemini_key
)

prompt_template = PromptTemplate.from_template(
    """
    Ти допомагаєш створювати текст для слайдів. 
    Заголовок слайда: {slide_heading}
    """
)

ai_chain = prompt_template | ai_model

# MediaPipe Hands
mp_hands_module = mp.solutions.hands
mp_drawer = mp.solutions.drawing_utils
camera = cv2.VideoCapture(0)

gesture_timer = None
hold_duration = 1
text_in_progress = None

# Основний цикл
with mp_hands_module.Hands(
        static_image_mode=False,
        max_num_hands=2,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
) as hand_detector:

    while True:
        ret, frame_img = camera.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)
        hand_results = hand_detector.process(rgb_frame)

        if hand_results.multi_hand_landmarks:
            for lm, hand_info in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
                mp_drawer.draw_landmarks(frame_img, lm, mp_hands_module.HAND_CONNECTIONS)

                hand_type = hand_info.classification[0].label
                if hand_type == "Right":
                    continue  # Аналізуємо лише ліву руку

                #  Координати
                thumb_tip = lm.landmark[4]
                thumb_mcp = lm.landmark[2]

                index_tip = lm.landmark[8]
                index_mcp = lm.landmark[5]
                index_pip = lm.landmark[6]
                index_dip = lm.landmark[7]

                middle_tip = lm.landmark[12]
                middle_mcp = lm.landmark[9]
                middle_pip = lm.landmark[10]
                middle_dip = lm.landmark[11]

                ring_tip = lm.landmark[16]
                ring_mcp = lm.landmark[13]
                ring_pip = lm.landmark[14]
                ring_dip = lm.landmark[15]

                pinky_tip = lm.landmark[20]
                pinky_mcp = lm.landmark[17]
                pinky_pip = lm.landmark[18]
                pinky_dip = lm.landmark[19]

                #  Жест
                fingers_folded_left = (
                    index_tip.y > index_mcp.y + 0.01 and
                    middle_tip.y > middle_mcp.y + 0.01 and
                    ring_tip.y > ring_mcp.y + 0.01 and
                    pinky_tip.y > pinky_mcp.y + 0.01
                )

                fingers_folded_right = (
                    index_tip.y < index_mcp.y - 0.01 and
                    middle_tip.y < middle_mcp.y - 0.01 and
                    ring_tip.y < ring_mcp.y - 0.01 and
                    pinky_tip.y < pinky_mcp.y - 0.01
                )

                avg_z_pos = (index_tip.z + middle_tip.z + ring_tip.z + pinky_tip.z + thumb_tip.z) / 5
                fingers_aligned = all(abs(l.z - avg_z_pos) < thresholds.z_tolerance for l in
                                      [thumb_tip, index_tip, middle_tip, ring_tip, pinky_tip])

                angles_ok = (
                    calculate_angle(index_dip, index_pip, index_mcp) < thresholds.max_finger_angle and
                    calculate_angle(middle_dip, middle_pip, middle_mcp) < thresholds.max_finger_angle and
                    calculate_angle(ring_dip, ring_pip, ring_mcp) < thresholds.max_finger_angle and
                    calculate_angle(pinky_dip, pinky_pip, pinky_mcp) < thresholds.max_finger_angle
                )

                thumb_left_extended = thumb_tip.x - thumb_mcp.x > thresholds.thumb_left
                thumb_right_extended = thumb_tip.x - thumb_mcp.x < thresholds.thumb_right

                thumb_side_left = thumb_tip.x > max(index_mcp.x, pinky_mcp.x)
                thumb_side_right = thumb_tip.x < min(index_mcp.x, pinky_mcp.x)

                thumb_up_gesture = (thumb_tip.y - thumb_mcp.y) < thresholds.thumb_up

                gesture_left = fingers_folded_left and fingers_aligned and thumb_left_extended and thumb_side_left and angles_ok
                gesture_right = fingers_folded_right and fingers_aligned and thumb_right_extended and thumb_side_right and angles_ok

                current_time = time.time()

                if gesture_left or gesture_right or (thumb_up_gesture and angles_ok):
                    if text_in_progress:
                        gesture_timer = None
                        continue

                    if gesture_timer is None:
                        gesture_timer = current_time
                    elif (current_time - gesture_timer) >= hold_duration:
                        if gesture_left:
                            previous_slide()
                            print("Left Slide Gesture")
                        elif gesture_right:
                            next_slide()
                            print("Right Slide Gesture")
                        else:
                            current_slide = ppt_window.View.Slide
                            slide_title = current_slide.Shapes.Title.TextFrame.TextRange.Text
                            text_in_progress = True

                            result_text = ai_chain.invoke({"slide_heading": slide_title})
                            current_slide.Shapes.Placeholders(2).TextFrame.TextRange.Text = result_text

                            text_in_progress = None
                            presentation.Save()
                            print("Thumb Up Gesture - Text Added")

                        gesture_timer = None
                else:
                    gesture_timer = None

        cv2.imshow("Camera Feed", frame_img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

camera.release()
presentation.Close()
ppt_app.Quit()
cv2.destroyAllWindows()
