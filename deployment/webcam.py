from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import cv2
import Demo
# from src.test import Demo
class DryHand(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DryHand')
        self.setGeometry(150,150,800,540)
        self.initUI()
        self.cont = True

    def startui(self):
        self.initUI()
    
    def initUI(self):
        self.fps = 60
        self.frame = QLabel(self)
        self.frame.resize(640, 480)
        self.frame.setScaledContents(True)
        self.frame.move(5,5)
        self.prt = QLabel(self)
        self.prt.resize(200, 25)
        self.prt.move(5 + 105 + 105, 490)
        
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

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Window Close', 'Are you sure?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.cont = False
            event.accept()
            print("window closed")
        else:
            event.ignore

    def imgdraw(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = QImage(img, img.shape[1], img.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.frame.setPixmap(pix)

        return self.cont