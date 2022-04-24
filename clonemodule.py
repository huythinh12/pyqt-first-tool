from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from research import Ui_MainWindow
import sys


class MainWindow(QMainWindow):
    def __init__(self):     
        super(MainWindow,self).__init__()
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.button = self.main_win.findChild(QPushButton,"pushButton")
        self.label = self.main_win.findChild(QLabel,"label")
        self.button.installEventFilter(self)
        self.button.clicked.connect(self.clicker)
        self.last_x, self.last_y = None, None

    def clicker(self):
        # fname = QFileDialog.getOpenFileName(self,"")
        print("xin chao")
    def show(self):
        self.main_win.show()


    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            
            return # Ignore the first time.

        painter = QPainter(self.label.pixmap())
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        # painter.
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()
    def paintEvent(self, e: QPaintEvent):
        QPainter.rota
    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

if __name__ == "__main__" :
    app = QApplication(sys.argv)


    window = MainWindow()
    window.show()

    sys.exit(app.exec_())