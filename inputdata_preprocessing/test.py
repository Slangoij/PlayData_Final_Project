from tensorflow.python.keras.backend import one_hot
import HandTrackingModule as htm
import numpy as np
import pandas as pd
import draw
import datetime
import cv2
import os
#####################################
cam_size = 640
#####################################

detector = htm.handDetector(maxHands=1, detectionCon=0.75)

cap = cv2.VideoCapture(0)
cap.set(3, cam_size)
cap.set(4, cam_size)

draw_arr = []
in_check = 0
out_check = 0
control_mode = False
Canvas = np.zeros((cam_size, cam_size, 3), np.uint8)

img_path = 'img'
csv_path = 'csv'

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = detector.findHands(img)
    landmark_list, bbox = detector.findPosition(img, draw=False)

    if landmark_list:
        out_check = 0
        fingers = detector.fingersUp()
        if 1 not in fingers[1:]:
            in_check += 1
            if in_check == 10:
                in_check = 0
                control_mode = True
        if control_mode:
            draw_arr.append(landmark_list[8][1:])
            cv2.circle(img, tuple(landmark_list[8][1:]), 7, (255,0,0), cv2.FILLED)
    else:
        out_check += 1
        if out_check == 10 and control_mode:
            control_mode = False
            if not control_mode:
                if len(draw_arr) <= 100:
                    draw_arr = draw_arr[10:-10] 
                    Canvas = draw.draw_canvas(Canvas, len(draw_arr), draw_arr)
                    draw_arr += [[0,0]] * (80 - len(draw_arr))

                    draw.save_file(Canvas, draw_arr, img_path, csv_path)
                    Canvas = np.zeros((cam_size, cam_size, 3), np.uint8)
                draw_arr.clear()


    cv2.imshow('img', img)
    cv2.waitKey(1)

