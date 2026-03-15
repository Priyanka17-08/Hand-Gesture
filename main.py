import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time

pyautogui.FAILSAFE = False

# Screen
screen_width, screen_height = pyautogui.size()

# MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.75,
                       min_tracking_confidence=0.75)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
smoothening = 18
mode = "MOUSE"
last_click_time = 0

def find_distance(p1, p2):
    return math.hypot(p2[0]-p1[0], p2[1]-p1[1])

while True:

    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame,1)
    h,w,c = frame.shape

    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            lm_list=[]

            for id,lm in enumerate(hand_landmarks.landmark):

                cx,cy=int(lm.x*w),int(lm.y*h)
                lm_list.append((id,cx,cy))

            mp_draw.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS)

            if len(lm_list)!=0:

                x_index,y_index=lm_list[8][1],lm_list[8][2]
                x_thumb,y_thumb=lm_list[4][1],lm_list[4][2]

                dist_thumb_index=find_distance((x_index,y_index),(x_thumb,y_thumb))

                index_up=lm_list[8][2]<lm_list[6][2]
                middle_up=lm_list[12][2]<lm_list[10][2]
                ring_up=lm_list[16][2]<lm_list[14][2]

                # SCROLL
                if index_up and not middle_up and not ring_up:

                    mode="SCROLL"

                    if y_index<h//2:
                        pyautogui.scroll(40)
                    else:
                        pyautogui.scroll(-40)

                # VOLUME
                elif not index_up and not middle_up:

                    mode="VOLUME"

                    if lm_list[4][2]<lm_list[3][2]:
                        pyautogui.press("volumeup")
                        time.sleep(0.2)

                    elif lm_list[4][2]>lm_list[3][2]:
                        pyautogui.press("volumedown")
                        time.sleep(0.2)

                # MOUSE
                elif index_up and middle_up:

                    mode="MOUSE"

                    screen_x=np.interp(x_index,(100,w-100),(0,screen_width))
                    screen_y=np.interp(y_index,(100,h-100),(0,screen_height))

                    curr_x=prev_x+(screen_x-prev_x)/smoothening
                    curr_y=prev_y+(screen_y-prev_y)/smoothening

                    pyautogui.moveTo(curr_x,curr_y)

                    prev_x,prev_y=curr_x,curr_y

                    # CLICK
                    if dist_thumb_index<30:

                        current_time=time.time()

                        if current_time-last_click_time>0.5:

                            pyautogui.click()

                            last_click_time=current_time

                else:
                    mode="MOUSE"

    cv2.rectangle(frame,(0,0),(350,70),(0,0,0),-1)

    cv2.putText(frame,f"MODE: {mode}",(10,45),
                cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)

    cv2.imshow("AI Hands-Free Control System",frame)

    if cv2.waitKey(1)&0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()