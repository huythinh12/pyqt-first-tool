from asyncio import events
from http.cookies import _quote
from turtle import update
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from tool_gui_core import Ui_MainWindow
import sys

# class Label(QWidget):
#     def __init__(self, parent=None):
#         QWidget.__init__(self, parent=parent)
#         self.p = QPixmap()

#     def setPixmap(self, p):
#         self.p = p
#         self.update()

#     def paintEvent(self, event):
#         if not self.p.isNull():
#             painter = QPainter(self)
#             painter.setRenderHint(QPainter.SmoothPixmapTransform)
#             painter.drawPixmap(self.rect(), self.p)


# class Widget(QMainWindow):
#     def __init__(self, parent=None):
#         QWidget.__init__(self, parent=parent)
#         lay = QVBoxLayout(self)
#         lb = Label(self)
#         lb.setPixmap(QPixmap("car.jpg"))
#         lay.addWidget(lb)

class MainWindow(QMainWindow):
    def __init__(self):
        
        QMainWindow.__init__(self)
        # super(MainWindow,self).__init__()
        self.setWindowTitle("Thinh.Nguyen App")
        # self.main_win = QMainWindow()
        # self.ui = uic.loadUi("toolgui.ui",self)
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.checkResize = False
        self.startDraw = False
        #test 
        # self.pixmap = QPixmap()
        # self.uic.label.setPixmap(self.pixmap)
    
        #-----

        #setting main win 
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.uic.label.setStyleSheet("background-color: rgba(255,255,255,0.1)")

        #find child in design
        # 
        # self.fileMenu = self.findChild(QMenuBar, "menubar")

        # #signal
        self.setWindowOpacity(0.8)
        self.openAction = self.findChild(QAction, "actionLoad")   
        self.exitAction = self.findChild(QAction, "actionExit")

        self.openAction.triggered.connect(self.openImage) 
        self.exitAction.triggered.connect(self.close)
        # self.uic.label.installEventFilter(self)
        # self.uic.labelDrag.installEventFilter(self)
        
        self.dragStart = False;
        
        #set Qlabel to centralwidget 
        # self.label = QLabel()
        # self.setCentralWidget(self.uic.label)
        # self.uic.label.setPixmap(self.)
        self.last_x, self.last_y = None, None
        
        # self.uic.pos1 = [0,0]
        # self.uic.pos2 =[0,0]
        # self.uic.label.setStyleSheet("background-color: rgba(255,255,255,1%);")


        
  
        
    #load img
    def openImage(self):
        self.startDraw = True
        imagePath, _ = QFileDialog.getOpenFileName()
        self.pixmap = QPixmap(imagePath)
        # self.pixmap.scaled(aspectRatioMode=ig)
        # self.uic.label.setPixmap(self.myscalePixmap)
        
        
        # self.uic.label.setScaledContents(True)
        self.savedPixmapSize = self.pixmap.size()
        self.resize(self.savedPixmapSize)
        
        # self.adjustSize()
        self.uic.label.setPixmap(self.pixmap)

        # self.uic.label.installEventFilter(self)
        
        #variable tracking
        self.checkResize = True
        # self.updateScaleContentPixmap = False



    def mousePressEvent(self, e: QMouseEvent):
        self.last_x = None
        self.last_y = None
        self.uic.label.setScaledContents(False)
        
        if e.button() == Qt.MouseButton.RightButton:
            print("xin")
            self.dragStart = True
            self.oldPos = e.globalPos() # xu ly drag 
        
    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.RightButton:
             self.dragStart = False
        else:
            # print("noneeeeee")
            #refresh point 
            self.last_x = None
            self.last_y = None
            
            #new add
            # self.update()  

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.dragStart:
            delta = QPoint(e.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = e.globalPos()
        elif self.startDraw:
            if self.last_x is None: # First event.
                self.last_x = e.x()
                self.last_y = e.y() 
                return # Ignore the first time.
            painter = QPainter(self.uic.label.pixmap())
            painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
            painter.end()
            self.update()
            
            # Update the origin for next time.
            self.last_x = e.x()
            self.last_y = e.y()


         
        
    # def paintEvent(self, e: QPaintEvent):
    #     print("xin")
    #     qp=QPainter(self.uic.label.pixmap())
    #     qp.begin(self)
    #     pen = QPen(Qt.black,5)
    #     qp.setPen(pen)
    #     qp.drawLine(self.pos1[0],self.pos1[1])
    #     qp.end()

    # paint with pythonguis - draw line
    # def mousePressEvent(self, e):
        
    #     self.pos1[0], self.pos1[1] = e.pos().x(),e.pos().y()
    #     self.update()

        # self.update()
        # self.uic.label.setText('Mouse button pressed at '+text)
        # print(f"coordinate: {text}")
        # self.update()



        # if self.last_x is None: # First event.
        #     self.last_x = e.x()
        #     self.last_y = e.y()
        #     print("nonnne")
        #     return # Ignore the first time.
        # print("thoat ra")
        # self.uic.label.setScaledContents(False)
        # self.reszie(self.uic.label.size())
        # pen = QPen(Qt.black,5)
        # pen.setWidth(20)

        # painter = QPainter(self.uic.label.pixmap())
        # painter.setPen(pen)

        # painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        # painter.end()

        # Update the origin for next time.
        # self.last_x = e.x()
        # self.last_y = e.y()
      

    def resizeEvent(self,e: QResizeEvent):
        self.uic.label.setScaledContents(True)
      
         
        
        # self.uic.label.setPixmap(self.pixmap.scaled(self.uic.label.width(),self.uic.label.height(),aspectRatioMode=0))

        # self.reszie(self.uic.label.size())
        # if self.pixmap:
        #     print("pixmapp chay")
        #     # print(f" sizee label {self.uic.label.x} ")
        #     self.pixmap.scaled(self.uic.label.size())
        
        # self.pixmap.scaled(self.width(), self.height())
        # self.uic.label.setPixmap(self.pixmap)
        # self.uic.label.resize(self.width(), self.height())
        # self.uic.label.setSizePolicy(QSizePolicy.expandingDirections,QSizePolicy.expandingDirections)
        if self.checkResize:
            
            self.myscalePixmap = self.pixmap.scaled(self.uic.label.size(),aspectRatioMode=0,transformMode=0)
            self.uic.label.setPixmap(self.myscalePixmap)
        
            # print("resize ")

        #    self.uic.label.setScaledContents(True)


            # self.uic.label.size(self.savedPixmapSize)
            # self.updateScaleContentPixmap = True
            # self.uic.label.setPixmap(self.myscalePixmap)
            # self.myscalePixmap = self.pixmap.scaled(self.uic.label.size(),aspectRatioMode=0,transformMode=0)
            # self.uic.label.setPixmap(self.myscalePixmap)
            # self.savedPixmapSize = self.pixmap.size()
            # self.uic.label.setPixmap(self.savedPixmapSize)
            # self.uic.label(self.pixmap.scaled(self.size()))

          

        
            

    # def mouseReleaseEvent(self, e:QMouseEvent):
    #     self.pos2[0],self.pos2[1] = e.pos().x(),e.pos().y()
    #     # self.last_x = None
    #     # self.last_y = None
    #     x = e.x()
    #     y = e.y()
    #     text = "x: {0}, y: {1}".format(x, y) 
    #     print(f"mouse release coordinate : {text}")
        # self.update()

        

#moi them vao
    # def setPixmap(self, p):
    #     self.p = p
    #     self.update()

    # def paintEvent(self, event):
    #     if not self.p.isNull():
    #         painter = QPainter(self)
    #         painter.setRenderHint(QPainter.SmoothPixmapTransform)
    #         painter.drawPixmap(self.rect(), self.p)

    #cach setup cũ
    # def show(self):
    #     self.main_win.show()

if __name__ == "__main__" :
    app = QApplication(sys.argv)


    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
    