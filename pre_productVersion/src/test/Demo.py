import sys
from common import HandTrackingModule as htm
from src import GestureModelModule as gmm
from src import AutopyClass
from tensorflow import keras
from common import draw
import numpy as np
import cv2
# from src.user_interface.webcam import DryHand as dr
from re import S
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class demopy():
    def __init__(self):
        #####################################
        # webcam size 지정
        self.hCam, self.wCam = 640, 640
        # model 설정 값 초기 정의
        self.model_name = 'vgg16_model_4cls_ws_id_2-3_noangle'
        self.model_selection = 'CNN'
        self.conf_limit = 0.75
        # self.imdraw = dr.imgdraw()
        # self.gesture_model = keras.models.load_model(r'./././model/saved_model/{0}.h5'.format(self.model_name))
        self.detector = htm.handDetector(maxHands=1, detectionCon=0.75)
        #####################################

    def demo(self, quitbutton=None):
        if quitbutton=='q':
            print(quitbutton)
            exit()

<<<<<<< HEAD:src/test/Demo.py
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        # webcam size 조정
        cap.set(3, self.wCam)
        cap.set(4, self.hCam)

        draw_arr = []
        in_check = 0
        out_check = 0
        control_mode = False
        

        while True:
            success, self.img = cap.read()
            self.img = cv2.flip(self.img, 1)
            
            # 이미지에서 손인식
            self.img = self.detector.findHands(self.img)
            landmark_list, bbox = self.detector.findPosition(self.img, draw=False)
=======
cap = cv2.VideoCapture(0)
# webcam size 조정
cap.set(3, wCam)
cap.set(4, hCam)

draw_arr = []
in_check = 0
out_check = 0
>>>>>>> develop:pre_productVersion/src/test/Demo.py

            # 손 인식 되면
            if landmark_list:
                out_check = 0
                fingers = self.detector.fingersUp()
                if 1 not in fingers[1:]:
                    # 주먹 쥐면 검지의 좌표 저장
                    in_check += 1
                    if in_check == 10:
                        in_check = 0
                        control_mode = True
                if control_mode:
                    draw_arr.append(landmark_list[8][1:])
                    cv2.circle(self.img, tuple(landmark_list[8][1:]), 7, (255,0,0), cv2.FILLED)
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
                            input_data, imgCanvas = gmm.trans_input(draw_arr, self.wCam, self.hCam, self.model_selection)
                            
                            # 예측률 75% 이상 input 데이터 저장
                            draw.save_file(imgCanvas, draw_arr)
                        draw_arr.clear()

<<<<<<< HEAD:src/test/Demo.py
            cv2.imshow('img', self.img)
            cv2.waitKey(0)
=======
    # 손 인식 되면
    if landmark_list:
        out_check = 0
        fingers = detector.fingersUp()
        # 검지 손가락만 펴져있으면 control mode
        control_mode = (fingers[1] == 1) and (1 not in fingers[2:])
        if control_mode:
            draw_arr.append(landmark_list[8][1:])
            cv2.circle(img, tuple(landmark_list[8][1:]), 7, (255,0,0), cv2.FILLED)
    else:
        # 손 인식 안되면
        out_check += 1
        if out_check == 10:
            if 30 < len(draw_arr) <= 100:
                # 저장한 좌표로 input 데이터 생성
                draw_arr = draw_arr[10:-10] # 앞, 뒤 10 frame 씩 제외
                # 모델 추론
                input_data, imgCanvas = gmm.trans_input(draw_arr, wCam, hCam, model_selection)
                pred, confidence = gmm.predict(gesture_model, input_data)
                
                # 예측률 75% 이상 input 데이터 저장
                if confidence > conf_limit:
                    AutopyClass.window_controller(pred)
                    draw.save_file(imgCanvas, draw_arr, pred)
                Canvas = np.zeros((wCam, hCam, 3), np.uint8)
            draw_arr.clear()
>>>>>>> develop:pre_productVersion/src/test/Demo.py


p = demopy()
p.demo()