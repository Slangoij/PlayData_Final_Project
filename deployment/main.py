from PyQt5.QtGui import QFont, QFontDatabase
<<<<<<< HEAD
from webcam import DryHand
=======
from userInterface import DryHand
>>>>>>> develop
from PyQt5.QtWidgets import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./Bahnschrift.ttf')
    app.setFont(QFont('Bahnschrift'))
    ex = DryHand()
    sys.exit(app.exec_())