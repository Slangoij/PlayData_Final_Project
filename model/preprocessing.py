from common import HandTrackingModule as htm
from common import draw as ds
import numpy as np
import pandas as pd
import cv2
#####################################
cam_size = 640
#####################################

detector = htm.handDetector(maxHands=1, detectionCon=0.75)
drawsave = ds.DrawSave()
cap = cv2.VideoCapture(0)
cap.set(3, cam_size)
cap.set(4, cam_size)

draw_arr = []
in_check = 0
out_check = 0
control_mode = False # 좌표 입력 모드 초기화
# 제스처 이동 궤적을 위한 Canvas 초기화
Canvas = np.zeros((cam_size, cam_size, 3), np.uint8) 

img_path = r'model/data/img/temp'
csv_path = r'model/data/csv/temp'

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    landmark_list, bbox = detector.findPosition(img, draw=False)

    if landmark_list:
        out_check = 0
        fingers = detector.fingersUp()
        # 주먹을 쥐면 좌표 입력 모드 True
        if 1 not in fingers[1:]:
            in_check += 1
            if in_check == 10:
                in_check = 0
                control_mode = True
        if control_mode:
            draw_arr.append(landmark_list[8][1:])
            cv2.circle(img, tuple(landmark_list[8][1:]), 7, (255,0,0), cv2.FILLED)
    # 손이 인식 안되면 입력 받은 좌표들로 데이터 생성
    else:
        out_check += 1
        if out_check == 10 and control_mode:
            control_mode = False
            if not control_mode:
                # 최소 20, 최대 100 frame 까지 입력 받기
                if 20 < len(draw_arr) <= 100:
                    draw_arr = draw_arr[10:-10] # 앞뒤로 10 frame 씩 무시
                    Canvas = drawsave.draw_canvas(Canvas, len(draw_arr), draw_arr)
                    draw_arr += [[0,0]] * (80 - len(draw_arr))

                    drawsave.save_file(Canvas, draw_arr, img_path, csv_path)
                    Canvas = np.zeros((cam_size, cam_size, 3), np.uint8)
                draw_arr.clear()


    cv2.imshow('img', img)
    cv2.waitKey(1)

