import numpy as np
import cv2
import HandTrackingModule as htm
import pandas as pd
import time
import datetime
import draw
import os
from AutopyClass import window_controller
from tensorflow import keras
from tensorflow.keras.preprocessing.image import img_to_array
####################################################################
# webcam 화면 사이즈 조정 파라미터
wCam, hCam = 640, 360
####################################################################
# 모델 호출
gesture_model = keras.models.load_model('./model/LSTM_model3-5.h5')

detector = htm.handDetector(maxHands=1, detectionCon=0.75)

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# model input값 초기화 이하 Canvas
Canvas = np.zeros((hCam, wCam, 3), np.uint8)
draw_arr = []
input_arr = [] # frame 저장 변수
check = 0

img_path  = 'img'

##############
prev_time = 0
FPS = 30
##############

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    landmark_list, bbox = detector.findPosition(img, draw=False)
    if landmark_list:
        fingers = detector.fingersUp()
    
    curr_time = time.time() - prev_time
    if (success) and (curr_time > 1. / FPS):
        prev_time = time.time()
    
        # 손 인식이 안되면 input_arr 초기화
        if len(landmark_list):
            check = 0
            if fingers[1] and fingers[4]:
                two_fingers = landmark_list[8][1:] + landmark_list[20][1:]
                input_arr.append(two_fingers)
                draw_arr.append(two_fingers)
            elif fingers[1]:
                input_arr.append(landmark_list[8][1:] + [0, 0])
                draw_arr.append(landmark_list[8][1:])

            if len(input_arr) == 20:
                input_data = np.array(input_arr)
                print(input_arr)
                # 제스처 그림 확인
                Canvas = draw.draw_canvas(Canvas, 20, draw_arr)
                t = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                cv2.imwrite(os.path.join(img_path, f'{t}.png'), Canvas)
                Canvas = np.zeros((hCam, wCam, 3), np.uint8)
                draw_arr.clear()
                # 모델 인풋에 맞춰 전처리
                input_data = input_data[np.newaxis, ...]
                pred = gesture_model.predict(input_data)
                print(pred)
                idx = np.argmax(pred[0])
                window_controller(idx)
                input_arr.clear()

        # 손 인식 되면 input_arr에 넣기
        else:
            check += 1
            if check > 5:
                check = 0
                input_arr.clear()
                draw_arr.clear()

    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


