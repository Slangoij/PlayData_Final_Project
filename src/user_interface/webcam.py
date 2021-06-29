from re import S
from PyQt5 import QtCore
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
from src.test import Demo

# from src.test import Demo

class DryHand(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DryHand')
        self.setGeometry(150,150,800,540)
        # self.detector = htm.handDetector(maxHands=1, detectionCon=0.75)
        self.initUI()
        self.cont = True

    def startui(self):
        self.initUI()
    
    def initUI(self):
        # self.cap = cv2.VideoCapture(0)
        # self.cap.set(3, 640)
        # self.cap.set(4, 640)
        self.fps = 60
        # self.sens = 300
        # # _, self.img_o = self.cpt.read()
        # self.cnt = 0
        self.frame = QLabel(self)
        self.frame.resize(640, 480)
        self.frame.setScaledContents(True)
        self.frame.move(5,5)

        # self.btn_on = QPushButton("입력 실행", self)
        # self.btn_on.resize(100, 25)
        # self.btn_on.move(5, 490)
        # # self.btn_on.clicked.connect(self.loadModel)
        # self.btn_on.clicked.connect(self.start)

        self.btn_off = QPushButton("입력 중지", self)
        self.btn_off.resize(100, 25)
        self.btn_off.move(5 + 100 + 5, 490)
    
        self.btn_off.clicked.connect(self.stop)
        

        self.prt = QLabel(self)
        self.prt.resize(200, 25)
        self.prt.move(5 + 105 + 105, 490)

        # self.sldr = QSlider(Qt.Horizontal, self)
        # self.sldr.resize(100, 25)
        # self.sldr.move(5 + 105 + 105 + 200, 490)
        # self.sldr.setMinimum(1)
        # self.sldr.setMaximum(30)
        # self.sldr.setValue(24)
        # self.sldr.valueChanged.connect(self.setFps)

        # self.sldr1 = QSlider(Qt.Horizontal, self)
        # self.sldr1.resize(100, 25)
        # self.sldr1.move(5 + 105 + 105 + 200 + 105, 490)
        # self.sldr1.setMinimum(50)
        # self.sldr1.setMaximum(500)
        # self.sldr1.setValue(300)
        # self.sldr1.valueChanged.connect(self.setSens)
        
        # 모드와 현재 동작 표기
        self.mode1 = QLabel("현재 모드", self)
        self.mode1.resize(150, 25)
        self.mode1.move(650, 50)
        
        self.mode2 = QLabel(self)
        self.mode2.resize(150, 25)
        self.mode2.move(650, 90)
        
        self.act1 = QLabel("현재 동작", self)
        self.act1.resize(150, 25)
        self.act1.move(650, 150)
        
        self.act2 = QLabel(self)
        self.act2.resize(150, 25)
        self.act2.move(650, 190)
        self.show()

    # def setFps(self):
    #     self.fps = self.sldr.value()
    #     self.prt.setText("FPS " + str(self.fps) + "로 조정")
    #     self.timer.stop()
    #     self.timer.start(1000. / self.fps)

    # def setSens(self):
    #     self.sens = self.sldr1.value()
    #     self.prt.setText("감도 " + str(self.sens) + "로 조정")
    


    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.cont = False
            event.accept()
            print("window closed")
        else:
            event.ignore

    def stop(self):
        self.frame.setPixmap(QPixmap.fromImage(QImage()))
        self.cont = False

    def imgdraw(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.frame.setPixmap(pix)

        return self.cont


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = DryHand()
    # ex = start.startui()
    global st
    st = Demo.demopy()
    ex = st.demo()

    # ex = DryHand()

    sys.exit(app.exec_())