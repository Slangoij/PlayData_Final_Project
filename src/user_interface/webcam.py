from re import S
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, cv2, numpy, time
from common import HandTrackingModule as htm
from src import GestureModelModule as gmm
from src import AutopyClass
from tensorflow import keras
from common import draw
import numpy as np
import cv2
# from src.test import Demo
from src.test import Demo_ij

class DryHand(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DryHand')
        self.setGeometry(150,150,900,540)
        self.initUI()
    
    def initUI(self):
        self.timer = QTimer()
        self.cpt = cv2.VideoCapture(0)
        self.fps = 24
        self.sens = 300
        self.win_width = 900
        self.win_height = 540
        self.frame_width = 640
        self.frame_height = 480
        self.btn_width = int((self.win_width-250)//2)
        self.btn_height = self.win_height-self.frame_height-20
        self.center_labels = 75

        self.frame = QLabel(self)
        self.frame.resize(self.frame_width, self.frame_height)
        self.frame.setScaledContents(True)
        self.frame.move(5,5)

        self.btn_on = QPushButton("입력 실행", self)
        self.btn_on.resize(self.btn_width, self.btn_height)
        self.btn_on.move(5, self.frame_height + 10)
        self.btn_on.clicked.connect(self.loadModel)
        self.btn_on.clicked.connect(self.start)

        self.btn_off = QPushButton("입력 중지", self)
        self.btn_off.resize(self.btn_width, self.btn_height)
        self.btn_off.move(5 + self.btn_width + 5, self.frame_height + 10)
        self.btn_off.clicked.connect(self.stop)

        self.prt = QLabel(self)
        self.prt.resize(200, 490)
        self.prt.move(5, self.frame_height + 10) # 5 +  (self.btn_width + 5)*2

        self.sldr = QSlider(Qt.Horizontal, self)
        self.sldr.resize(100, 25)
        self.sldr.move(self.win_width-105-105, self.win_height-self.btn_height*2)
        self.sldr.setMinimum(1)
        self.sldr.setMaximum(30)
        self.sldr.setValue(24)
        self.sldr.valueChanged.connect(self.setFps)

        self.sldr1 = QSlider(Qt.Horizontal, self)
        self.sldr1.resize(100, 25)
        self.sldr1.move(self.win_width-105, self.win_height-self.btn_height*2)
        self.sldr1.setMinimum(50)
        self.sldr1.setMaximum(500)
        self.sldr1.setValue(300)
        self.sldr1.valueChanged.connect(self.setSens)
        
        # 모드와 현재 동작 표기
        self.mode1 = QLabel("현재 모드", self)
        self.mode1.resize(150, 25)
        self.mode1.move(self.frame_width + (self.win_width-self.frame_width)//2 - self.center_labels, 100)
        
        self.mode2 = QLabel(self)
        self.mode2.resize(150, 25)
        self.mode2.move(self.frame_width + (self.win_width-self.frame_width)//2 - self.center_labels, 140)
        
        self.mode3 = QLabel(self)
        self.mode3.resize(150, 25)
        self.mode3.move(self.frame_width + (self.win_width-self.frame_width)//2 - self.center_labels + 100, 140)
        
        self.act1 = QLabel("현재 동작", self)
        self.act1.resize(150, 25)
        self.act1.move(self.frame_width + (self.win_width-self.frame_width)//2 - self.center_labels, 250)
        
        self.act2 = QLabel(self)
        self.act2.resize(150, 25)
        self.act2.move(self.frame_width + (self.win_width-self.frame_width)//2 - self.center_labels, 300)

        self.show()

    def setFps(self):
        self.fps = self.sldr.value()
        self.prt.setText("FPS " + str(self.fps) + "로 조정")
        self.timer.stop()
        self.timer.start(1000. / self.fps)

    def setSens(self):
        self.sens = self.sldr1.value()
        self.prt.setText("감도 " + str(self.sens) + "로 조정")
    
    def start(self):
        self.timer.timeout.connect(self.predict)
        self.timer.start(1000 / self.fps)

    def stop(self):
        self.frame.setPixmap(QPixmap.fromImage(QImage()))
        self.timer.stop()

    def loadModel(self):
        self.dpDemo_ij.demopy()

    def predict(self):
        # 모델 추론 및 UI에 영상 출력
        _, self.cam = self.cpt.read()
        self.cam = cv2.flip(self.cam, 1)

        # 손 인식시
        self.cam = self.detector.findHands(self.cam)
        self.landmark_list, bbox = self.detector.findPosition(self.cam, draw=False)

        if self.landmark_list:
            self.out_check = 0
            self.fingers = self.detector.fingersUp()
            if 1 not in self.fingers[1:]:
                # 주먹 쥐면 검지의 좌표 저장
                self.in_check += 1
                if self.in_check == 10:
                    self.in_check = 0
                    self.control_mode = True        
            if self.control_mode:
                self.draw_arr.append(self.landmark_list[8][1:])
                cv2.circle(self.cam, tuple(self.landmark_list[8][1:]), 7, (255,0,0), cv2.FILLED)
        else:
            self.out_check += 1
            if self.out_check == 10 and self.control_mode:
                self.control_mode = False
                if not self.control_mode:
                    if 20 < len(self.draw_arr) <= 100:
                        # 저장한 좌표로 input 데이터 생성
                        # 모델 추론
                        self.draw_arr = self.draw_arr[10:-10] # 앞, 뒤 10 frame 씩 제외
                        input_data, imgCanvas = gmm.trans_input(self.draw_arr, self.wCam, self.hCam, self.model_selection)
                        pred, confidence = gmm.predict(self.gesture_model, input_data)
                        
                        if confidence > self.conf_limit:
                            self.act2.setText(AutopyClass.window_controller(pred))
                        Canvas = np.zeros((self.wCam, self.hCam, 3), np.uint8)
                    self.draw_arr.clear()

        if Demo_ij.demopy:
            self.mode2.setText("입력모드")
            self.mode3.setText("")
        else:
            self.mode2.setText("")
            self.mode3.setText("입력모드X")
        
        # GUI에 이미지 출력
        self.cam = cv2.cvtColor(self.cam, cv2.COLOR_BGR2RGB)
        img = QImage(self.cam, self.cam.shape[1], self.cam.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.frame.setPixmap(pix)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DryHand()
    sys.exit(app.exec_())