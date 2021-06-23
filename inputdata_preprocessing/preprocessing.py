import numpy as np
import cv2
import HandTrackingModule as htm
import os
import datetime
import pandas as pd
from AutopyClass import window_controller
from tensorflow import keras
from tensorflow.keras.preprocessing.image import img_to_array
####################################################################
# webcam 화면 사이즈 조정 파라미터
wCam, hCam = 1280, 720
####################################################################

# 모델 호출
gesture_model = keras.models.load_model('./model/vgg16_model_3.h5')

detector = htm.handDetector(maxHands=1, detectionCon=0.75)

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# model input값 초기화 이하 Canvas
Canvas = np.zeros((hCam, wCam, 3), np.uint8)
input_arr = [] # frame 저장 변수
line_color = (255, 255, 255)
line_thickness = 10
finger_num = 8

csv_path = './csv'
img_path = './img'

csv_list = []
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    landmark_list, bbox = detector.findPosition(img, draw=False)
    
    # 손 인식이 안되면 input_arr 초기화
    if len(landmark_list) == 0:
        input_arr = []

    # 손 인식 되면 input_arr에 넣기
    else:
        if len(input_arr) < 30:
            input_arr.append(landmark_list[finger_num][1:])
        # input_arr 길이가 30이면  Canvas에 그리기
        if len(input_arr) >= 30:
            # csv_list.append(input_arr)
            prev_x, prev_y = input_arr[0]
            for i in range(1, 30):
                curr_x, curr_y = input_arr[i]
                cv2.line(Canvas, (prev_x, prev_y), (curr_x, curr_y), line_color, line_thickness)
                prev_x, prev_y = curr_x, curr_y

            print(prev_x, prev_y)
            # output값을 보기 위한 png파일 변환
            t = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            df = pd.DataFrame(input_arr)
            df.to_csv(os.path.join(csv_path, f'{t}.csv'), index=False, header=False)
            cv2.imwrite(os.path.join(img_path, f'{t}.png'), Canvas)
            
            # 모델 input 전처리
            Canvas = cv2.resize(Canvas, (640, 360))
            Canvas = img_to_array(Canvas)
            Canvas = Canvas[np.newaxis, ...]
            Canvas = Canvas/255.
            pred = gesture_model.predict(Canvas)
            print('#######################')
            print(pred)
            idx = np.argmax(pred[0])
            print(idx)
            print('#######################')
            window_controller(idx)
            Canvas = np.zeros((hCam, wCam, 3), np.uint8) # Canvas 초기화
            
            # 먼저 들어온 데이터 빼기(수정 필요)
            input_arr = input_arr[3:]

    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        # csv_list = np.array(csv_list)
        # csv_list = pd.DataFrame(csv_list)
        # csv_list.to_csv('next.csv', index=False, header=False)
        break
cap.release()
cv2.destroyAllWindows()


