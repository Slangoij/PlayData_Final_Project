from common import HandTrackingModule as htm
from src import GestureModelModule
from tensorflow import keras
from common import draw
import numpy as np
import cv2
#####################################
# webcam size 지정
hCam, wCam = 640, 640
#####################################

gesture_model = keras.models.load_model(r'./././model/saved_model/LSTM_model3-11.h5')
detector = htm.handDetector(maxHands=1, detectionCon=0.75)

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

draw_arr = []
in_check = 0
out_check = 0
control_mode = False

img_path = r'model/data/img/temp'
csv_path = r'model/data/csv/temp'

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    landmark_list, bbox = detector.findPosition(img, draw=False)

    if landmark_list:
        # 손 인식 되면
        out_check = 0
        fingers = detector.fingersUp()
        if 1 not in fingers[1:]:
            # 주먹 쥐면 검지의 좌표 저장
            in_check += 1
            if in_check == 10:
                in_check = 0
                control_mode = True
        if control_mode:
            draw_arr.append(landmark_list[8][1:])
            cv2.circle(img, tuple(landmark_list[8][1:]), 7, (255,0,0), cv2.FILLED)
    else:
        # 손 인식 안되면
        out_check += 1
        if out_check == 10 and control_mode:
            control_mode = False
            if not control_mode:
                if 20 < len(draw_arr) <= 100:
                    # 저장한 좌표로 input 데이터 생성
                    # 모델 추론
                    draw_arr = draw_arr[10:-10] # 앞, 뒤 10 frame 씩 제외
                    input_data, imgCanvas = GestureModelModule.trans_input(draw_arr, wCam, hCam, RNN=True)
                    pred, confidence = GestureModelModule.predict(gesture_model, input_data)
                    # 예측률 75% 이상 input 데이터 저장
                    if confidence > 0.75:
                        draw.save_file(imgCanvas, draw_arr, img_path, pred)
                    Canvas = np.zeros((wCam, hCam, 3), np.uint8)
                draw_arr.clear()

    cv2.imshow('img', img)
    cv2.waitKey(1)

