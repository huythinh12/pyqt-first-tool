import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from research import *
# from PySide2.QtCore import *
# from PySide2.QtGui import *
# from PySide2.QtWidgets import *


class LayoutFrame(QMainWindow):

    def __init__(self):

        super(LayoutFrame, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui = uic.loadUi('mainUi.ui', self)
        # self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setAttribute(Qt.WA_DeleteOnClose)
        # self.ui.setWindowOpacity(1)#0.5
        self.pixmap = QtGui.QPixmap('car.jpg')
        self.ui.label.setPixmap(self.pixmap)
        self.resize(self.pixmap.size())

        # self.ui.label.setPixmap(self.pixmap.scaled(self.size()))
        self.ui.label.setStyleSheet("background-color: rgba(255,255,255,1%);")
        self.last_x, self.last_y = None, None

        # self.ui.label.setStyleSheet("background-color: rgba(255,255,255,100%);")
        self.ui.label.installEventFilter(self)
        self.ui.labelFrameMove.installEventFilter(self)

        self.ui.buttonExit.clicked.connect(self.close)
        
        QSizeGrip(self.ui.labelFrameResize)
        
        self.ui.sliderOpacity.valueChanged.connect(self.change_opacity)

        self.dragPos = QPoint()



    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return # Ignore the first time.
        painter = QtGui.QPainter(self.ui.label.pixmap())
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None



    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        print("xin chao")

    def eventFilter(self, source, event):
        #nut move 
        # if source == self.ui.labelFrameMove and event.type() == QEvent.MouseMove:
        #     if event.button() == Qt.LeftButton:
        #         self.move(self.pos() + event.globalPos() - self.dragPos)
        #         self.dragPos = event.globalPos()
        #         event.accept()

        if (source is self and event.type() == QEvent.Resize):
            self.ui.label(self.pixmap.scaled(self.size()))

        return False

    def change_opacity(self, value):
        new_pix = QtGui.QPixmap(self.pixmap.size())
        new_pix.fill(Qt.transparent)
        painter = QtGui.QPainter(new_pix)
        painter.setOpacity(value * 0.01)
        painter.drawPixmap(QPoint(), self.pixmap)
        painter.end()
        self.ui.label.setPixmap(new_pix)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = LayoutFrame()
    w.show()

    sys.exit(app.exec_())