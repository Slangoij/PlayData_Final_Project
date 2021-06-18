import numpy as np
import cv2
import HandTrackingModule as htm
import os
import time
import datetime

####################################################################
# webcam 화면 사이즈 조정 파라미터
wCam, hCam = 640, 360
####################################################################

detector = htm.handDetector(detectionCon=0.75, maxHands=1)

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# model input값 초기화 이하 Canvas
Canvas = np.zeros((hCam, wCam, 3), np.uint8)
input_arr = []  # frame 저장 변수
line_thickness = 3
line_color = (255, 255, 255)
finger_num = 8

########
prev_time = 0
FPS = 30
########

img_path = './img'

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    landmark_list, bbox = detector.findPosition(img, draw=False)

    curr_time = time.time() - prev_time
    # 초당 프레임수 제한.
    if (success is True) and (curr_time > 1. / FPS):
        prev_time = time.time()

        # 손 인식이 안되면 input_arr 초기화
        if len(landmark_list) == 0:
            if input_arr:
                prev_x, prev_y = input_arr[0]
                for i in range(len(input_arr)):
                    curr_x, curr_y = input_arr[i]
                    cv2.line(Canvas, (prev_x, prev_y), (curr_x, curr_y), line_color, line_thickness)
                    prev_x, prev_y = curr_x, curr_y

                # output값을 보기 위한 png파일 변환
                t = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                cv2.imwrite(os.path.join(img_path, f'{t}.png'), Canvas)
                Canvas = np.zeros((hCam, wCam, 3), np.uint8)  # Canvas 초기화
                input_arr.clear()

        # 손 인식 되면 input_arr에 넣기
        else:
            if len(input_arr) < 30:
                input_arr.append(landmark_list[finger_num][1:])
            # input_arr 길이가 30이면  Canvas에 그리기
            if len(input_arr) == 30:
                prev_x, prev_y = input_arr[0]
                trans_color = 5  # 색 변화를 위해
                for i in range(1, 30):
                    curr_x, curr_y = input_arr[i]
                    cv2.line(Canvas, (prev_x, prev_y), (curr_x, curr_y), line_color, line_thickness)
                    prev_x, prev_y = curr_x, curr_y

                # output값을 보기 위한 png파일 변환
                t = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                cv2.imwrite(os.path.join(img_path, f'{t}.png'), Canvas)
                Canvas = np.zeros((hCam, wCam, 3), np.uint8)  # Canvas 초기화

                # 먼저 들어온 데이터 빼기
                input_arr = input_arr[10:]

    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q'):
        break
