from Demo import demopy
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    st = demopy()
    ex = st.demo()
    sys.exit(app.exec_())