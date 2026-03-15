import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ------------------ Volume Setup ------------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# ------------------ Screen ------------------
screen_width, screen_height = pyautogui.size()

# ------------------ MediaPipe ------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.75,
                       min_tracking_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
smoothening = 7
mode = "MOUSE"

def find_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if lm_list:
                x1, y1 = lm_list[8][1], lm_list[8][2]   # Index
                x2, y2 = lm_list[4][1], lm_list[4][2]   # Thumb
                x3, y3 = lm_list[12][1], lm_list[12][2] # Middle

                # ------------------ MODE SWITCH ------------------
                dist_index_middle = find_distance((x1, y1), (x3, y3))
                dist_thumb_index = find_distance((x1, y1), (x2, y2))

                if dist_index_middle < 25:
                    mode = "SCROLL"

                elif dist_thumb_index < 25:
                    mode = "VOLUME"

                elif y1 < y3 and dist_index_middle > 40:
                    mode = "MOUSE"

                # ------------------ MOUSE MODE ------------------
                if mode == "MOUSE":
                    screen_x = np.interp(x1, (100, w - 100), (0, screen_width))
                    screen_y = np.interp(y1, (100, h - 100), (0, screen_height))

                    curr_x = prev_x + (screen_x - prev_x) / smoothening
                    curr_y = prev_y + (screen_y - prev_y) / smoothening

                    pyautogui.moveTo(curr_x, curr_y)
                    prev_x, prev_y = curr_x, curr_y

                    if dist_thumb_index < 30:
                        pyautogui.click()
                        time.sleep(0.3)

                # ------------------ SCROLL MODE ------------------
                elif mode == "SCROLL":
                    if y3 < y1 - 30:
                        pyautogui.scroll(30)
                    elif y3 > y1 + 30:
                        pyautogui.scroll(-30)

                # ------------------ VOLUME MODE ------------------
                elif mode == "VOLUME":
                    vol = np.interp(dist_thumb_index, [20, 200], [minVol, maxVol])
                    volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(frame, (0, 0), (350, 70), (0, 0, 0), -1)
    cv2.putText(frame, f"MODE: {mode}", (10, 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("AI Hands-Free Control System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()