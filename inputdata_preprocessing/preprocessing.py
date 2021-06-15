import numpy as np
import cv2
import HandTrackingModule as htm
import os
####################################################################
# webcam 화면 사이즈 조정 파라미터
wCam, hCam = 1280, 720
####################################################################

detector = htm.handDetector(maxHands=1, detectionCon=0.75)

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# model input값 초기화 이하 Canvas
Canvas = np.zeros((720, 1280, 3), np.uint8)
input_arr = [] # frame 저장 변수

img_path = './img'
file_name_cnt = 0 # img파일 이름 중복 방지
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
        if len(input_arr) < 40:
            input_arr.append(landmark_list[8][1:])
        # input_arr 길이가 40이면  Canvas에 그리기
        if len(input_arr) == 40:
            prev_x, prev_y = input_arr[0]
            trans_color = 5 # 색 변화를 위해
            for i in range(1, 40):
                curr_x, curr_y = input_arr[i]
                cv2.line(Canvas, (prev_x, prev_y), (curr_x, curr_y), (255, 0, trans_color), 15)
                prev_x, prev_y = curr_x, curr_y
                trans_color += 5

            # output값을 보기 위한 png파일 변환
            cv2.imwrite(os.path.join(img_path, f'img{file_name_cnt}.png'), Canvas)
            file_name_cnt += 1
            Canvas = np.zeros((720, 1280, 3), np.uint8) # Canvas 초기화
            
            # 먼저 들어온 데이터 빼기(수정 필요)
            for _ in range(2):
                input_arr.pop(0)

    cv2.imshow('img', img)
    cv2.waitKey(1)

