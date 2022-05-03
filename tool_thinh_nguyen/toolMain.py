import sys
from enum import Enum
from PySide2.QtGui import QPainter,QPen,QIcon ,QImage,QColor,QMouseEvent,QResizeEvent
from PySide2.QtWidgets import QApplication,QWidget,QHBoxLayout,QLabel,QSizeGrip,QVBoxLayout,QGraphicsOpacityEffect,QMainWindow,QGridLayout,QAction,QGroupBox,QRadioButton,QSlider,QFileDialog,QMessageBox,QColorDialog,QPushButton
from PySide2.QtCore import QPoint,Qt,QEvent,QObject,QSize,QCoreApplication 


"""
Tạo các type để vẽ 
"""
class DrawMode(Enum):
    Point = 1
    Line = 2

class FrameResize(QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(20)
        self.setMinimumHeight(20)
        self.hbox = QHBoxLayout(self)
        
        self.labelResize = QLabel(self)
        self.labelResize.setText("[ Resize Here ]")
        self.labelResize.setStyleSheet("background-color: rgba(181, 255, 216, 0.2); color:rgba(0, 0, 0, 1)")
        
        self.qSize = QSizeGrip(self.labelResize)
        self.qSize.resize(self.labelResize.width(),self.labelResize.height())
        
        
        self.hbox.addWidget(self.labelResize,0, Qt.AlignRight|Qt.AlignBottom)
        self.hbox.setContentsMargins(0,0,2,0)
        self.setLayout(self.hbox)

        
        

"""
tạo ra vùng tool box nằm bên trái window 
"""
class ToolBox(QWidget):
    def __init__(self):
        super().__init__()
        
        """
        cài đặt vùng tool box theo giá trị mặc định
        """
        self.setMaximumWidth(120)
        self.setMinimumWidth(50)
        self.setStyleSheet("background-color : rgba(233, 242, 255, 0.8)")
        """
        sử dụng vertical layout box cho vùng tool
        """
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)



"""
tạo ra vùng drawving riêng biệt với window
"""
class DrawingArea(QWidget):
    def __init__(self):
        super().__init__()
        self.dragStart = False 
        
        """
        tạo ra 2 img để dùng cho resize và undo
        """
        
        self.resizeSavedImage = QImage(0, 0, QImage.Format_RGB32)#width ,height , format color
        self.savedImage = QImage(0, 0, QImage.Format_RGB32)

        """
        cài đặt default cho opacity
        """
        self.opacity = 1;
        """
        cài đặt default cho image
        """
        self.currentImg = "rule3.png"
        self.image = QImage(self.width(), self.height(), QImage.Format_RGB32)
        self.image.load(self.currentImg)
        self.resizeSavedImage = self.image # lưu vào resize để khi scale img sẽ dc update theo và ko bị vỡ hình
        self.currentClear = self.image

 
        """
        cài đặt default cho brush 
        """
        self.drawing = False
        self.brushSize = 1
        self.brushColor = Qt.black
        self.brushStyle = Qt.SolidLine
        self.brushCap = Qt.RoundCap # đường nét kết thúc 
        self.brushJoin = Qt.RoundJoin # đường nét gấp khúc
        self.drawMode = DrawMode.Point

        """
        khởi tạo point để sử dụng cho drawline sau
        setMiniumWidth để img có độ rộng tối thiểu khi hiển thị lên màn hình
        """
        self.lastPoint = QPoint()
        self.setMinimumWidth(150)


    """
    update img khi nó được scale với 1 size khác thông qua resizeEvent
    """
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())
        
    def opacityDrawZone(self,value):
        op=QGraphicsOpacityEffect(self)
        op.setOpacity(self.opacity) #0 to 1 will cause the fade effect
        self.setGraphicsEffect(op)
        self.setAutoFillBackground(False)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            """
            draw mode là point sẽ vẽ từ con trỏ chuột lúc bắt đầu
            """
            if self.drawMode == DrawMode.Point:
                painter = QPainter(self.image) 
                painter.setPen(QPen(self.brushColor, self.brushSize, self.brushStyle, self.brushCap, self.brushJoin))
                painter.drawPoint(event.pos())
                self.drawing = True  # cho phép vẽ nếu là left click
                self.lastPoint = event.pos()  # new poit save vào last point
            elif self.drawMode == DrawMode.Line:
                """
                xử lý khi ko phải là draw mode point 
                """
                if self.lastPoint == QPoint():
                    self.lastPoint = event.pos()
                else:
                    painter = QPainter(self.image)  
                    painter.setPen(QPen(self.brushColor, self.brushSize, self.brushStyle, self.brushCap, self.brushJoin))
                    painter.drawLine(self.lastPoint, event.pos())
                    self.lastPoint = QPoint()

            """
            update khi có bất kỳ sự thay đổi nào
            """
            self.update()

    """
    mouseMove chỉ xử lý giành cho draw mode =  Point
    """

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing & (self.drawMode == DrawMode.Point):
            painter = QPainter(self.image)  
            painter.setPen(QPen(self.brushColor, self.brushSize, self.brushStyle, self.brushCap, self.brushJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()


    
    def mouseReleaseEvent(self, event):

        if event.button == Qt.LeftButton:
            """
            mỗi khi mouse release saved lại image để dùng cho undo
            """
            self.savedImage = self.resizeSavedImage
            self.resizeSavedImage = self.image
            self.drawing = False

    """
    dùng để hiển thị img và sẽ auto update vẽ lại cái img này mỗi khi có thay đổi
    lưu ý cái img này chính là để drawzone
    """
    def paintEvent(self, event):
        
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())


"""
main window của chương trình
"""
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        
 
        self.dragStart = False
        self.isTransParent = False
        
        self.setWindowTitle("Tool Main")
        self.setGeometry(100, 100,800, 600)  # top, left, width, height
        self.setWindowIcon(QIcon("./icons/paint-brush.png"))
        self.setStyleSheet("background-color: rgba(255,255,255,0.01)") 
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)
        """
        Khởi tạo layout cho window và gọi các function cho từng  chức năng 
        """
        self.grid = QGridLayout()
        self.box = ToolBox()
        self.frameResize = FrameResize()
        self.imageArea = DrawingArea()
        self.setMoveTool()
        self.setBrushSlider()
        self.setBrushStyle()
        self.setOpacitySlider()
        # self.setBrushCap()
        # self.setBrushJoin()
        self.setColorChanger()
        
        """
        tạo grid cho toàn window 
        """
        
        self.grid.addWidget(self.box, 0, 0, 1, 1) #Qwidget ,int r, int cl, int rspan,int clspan
        self.grid.addWidget(self.imageArea, 0, 1, 1, 6)
        self.grid.addWidget(self.frameResize,1,1,1,6)
        
        
        self.grid.setContentsMargins(0,0,0,0)
        self.grid.setVerticalSpacing(0)
        self.grid.setHorizontalSpacing(0)

        win = QWidget()
        win.setLayout(self.grid)
        self.setCentralWidget(win)


     

        """
        tạo menubar
        """
        # menus
        mainMenu = self.menuBar()
        mainMenu.installEventFilter(self)
        # set style for menu 
        mainMenu.setStyleSheet(
        """
        QMenuBar { background-color: rgba(233, 242, 255, 0.8)}


        QMenu {
            background-color:  rgb(255, 255, 255,1);   
        
            margin: 2px;
            }

        QMenu::item {
            background-color: transparent;
            }

        QMenu::item:selected { 
            background-color: rgba(233, 242, 255, 0.8);
            color: rgb(0,0,0);
            }
        """)

        mainMenu.setStyle
        fileMenu = mainMenu.addMenu(" File")  # the space is required as "File" is reserved in Mac
        drawMenu = mainMenu.addMenu("Draw")
        helpMenu = mainMenu.addMenu("Help")

        """
        tạo save và add vào file menu
        """
        saveAction = QAction("Save", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        """
        khi menu được chọn thì shortcut cũng sẽ trigger
        """
        saveAction.triggered.connect(self.save)

        """
        tạo open và add vào file menu
        """
        openAction = QAction(QIcon("./icons/open.png"), "Open", self)
        openAction.setShortcut("Ctrl+O")
        fileMenu.addAction(openAction)

        openAction.triggered.connect(self.open)

        """
        tạo undo và add vào file menu
        """
        undoAction = QAction(QIcon("./icons/undo.png"), "Undo", self)
        undoAction.setShortcut("Ctrl+Z")
        fileMenu.addAction(undoAction)
        undoAction.triggered.connect(self.undo)

        """
        tạo clear và add vào file menu
        """
        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        """
        tao exit va add vao file  menu.
        """
        exitAction = QAction(QIcon("./icons/exit.png"), "Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exitProgram)

        """
        tạo draw và add vào draw  menu.
        """
        self.pointAction = QAction("Point", self, checkable=True)
        self.pointAction.setShortcut("Ctrl+P")
        self.pointAction.setChecked(True)
        drawMenu.addAction(self.pointAction)
   
        self.pointAction.triggered.connect(lambda: self.changeDrawMode(self.pointAction))

        """
        tạo draw line và add vào draw menu.
        """
        self.lineAction = QAction("Line", self, checkable=True)
        self.lineAction.setShortcut("Ctrl+L")
        drawMenu.addAction(self.lineAction)
   
        self.lineAction.triggered.connect(lambda: self.changeDrawMode(self.lineAction))

        """
       tạo action aobout và add vào  "Help" menu.
        """
        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+I")
        helpMenu.addAction(aboutAction)
        self.msg = QMessageBox()
        self.msg.setStyleSheet("background-color: rgb(255,255,255)")
        aboutAction.triggered.connect(self.about)

        """
        update với setting default
        """
        self.imageArea.update()

   


    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            self.dragStart = True
            self.oldPos = e.globalPos()
    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.MouseButton.LeftButton:
            self.dragStart = False 

    def getPosFromDrawingZone(self,oldpos):
        print(f"old pos {oldpos}")
    """
    thay đổi draw mode
    """
    def changeDrawMode(self, check):
        if check.text() == "Point":
            self.pointAction.setChecked(True)
            self.lineAction.setChecked(False)
            self.imageArea.drawMode = DrawMode.Point
        elif check.text() == "Line":
            self.pointAction.setChecked(False)
            self.lineAction.setChecked(True)
            self.imageArea.drawMode = DrawMode.Line
        self.update()
        """
        Resets lại Qpoint nếu ko nó vẫn sẽ nối tiếp từ draw mode này sang drawmode kia
        """
        print(QPoint() )
        self.imageArea.lastPoint = QPoint()

    """
    tạo layout choh groupbox cho type brush
    """
    def setBrushStyle(self):
        self.brush_line_type = QGroupBox("Brush style")
        self.brush_line_type.setMaximumHeight(100)
        self.brush_line_type.setMinimumHeight(50)

        """
        Type của brush
        """
        self.styleBtn1 = QRadioButton(" Solid")
        self.styleBtn1.setIcon(QIcon("./icons/solid.png"))
        self.styleBtn1.setIconSize(QSize(32, 64))
        self.styleBtn1.clicked.connect(lambda: self.changeBrushStyle(self.styleBtn1))

        self.styleBtn2 = QRadioButton(" Dash")
        self.styleBtn2.setIcon(QIcon("./icons/dash.png"))
        self.styleBtn2.setIconSize(QSize(32, 64))
        self.styleBtn2.clicked.connect(lambda: self.changeBrushStyle(self.styleBtn2))

        self.styleBtn3 = QRadioButton(" Dot")
        self.styleBtn3.setIcon(QIcon("./icons/dot.png"))
        self.styleBtn3.setIconSize(QSize(32, 64))
        self.styleBtn3.clicked.connect(lambda: self.changeBrushStyle(self.styleBtn3))

        """
        add widget vào trong layout 
        """
        self.styleBtn1.setChecked(True)
        qv = QVBoxLayout()
        qv.addWidget(self.styleBtn1)
        qv.addWidget(self.styleBtn2)
        qv.addWidget(self.styleBtn3)
        self.brush_line_type.setLayout(qv)
        self.box.vbox.addWidget(self.brush_line_type)


    """
    lựa chọn type setting để vẽ
    """
    def changeBrushStyle(self, btn):
        if btn.text() == " Solid":
            if btn.isChecked():
                self.imageArea.brushStyle = Qt.SolidLine
        if btn.text() == " Dash":
            if btn.isChecked():
                self.imageArea.brushStyle = Qt.DashLine
        if btn.text() == " Dot":
            if btn.isChecked():
                self.imageArea.brushStyle = Qt.DotLine

    def setMoveTool(self):
        self.groupBox= QGroupBox("Move Tool")        
        self.groupBox.setMaximumHeight(50)
        self.moveLabel = QLabel("--->Drag Me<---- ")
        self.moveLabel.setStyleSheet("""background-color: rgba(181, 255, 216, 0.8);""")
        self.moveLabel.resize(self.groupBox.width(), self.groupBox.height())
        self.moveLabel.installEventFilter(self)

        qv = QVBoxLayout()
        qv.addWidget(self.moveLabel)
        self.groupBox.setLayout(qv)
        self.box.vbox.addWidget(self.groupBox)
    
    def eventFilter(self, obj: 'QObject', event: 'QEvent'):
    
        if obj == self.moveLabel and event.type() == QEvent.MouseMove:
      
            # self.oldPos = event.globalPos()
            # # else:
            self.move(self.pos() + event.globalPos() - self.oldPos)
            self.oldPos = event.globalPos()
            event.accept()
        return False

    """
    Tạo layout để chứa brush size
    """
    def setBrushSlider(self):
        self.groupBoxSlider = QGroupBox("Brush size")
        self.groupBoxSlider.setMaximumHeight(70)
        self.groupBoxSlider.setMinimumHeight(50)

        """
        cài đặt giá trị 1-40 cho slide brush
        """
        self.brush_thickness = QSlider(Qt.Horizontal)
        self.brush_thickness.setMinimum(1)
        self.brush_thickness.setMaximum(40)
        self.brush_thickness.valueChanged.connect(self.sizeSliderChange)

        """
        hiển thị thông số size của brush
        """
        self.brushSizeLabel = QLabel()
        self.brushSizeLabel.setText("%s px" % self.imageArea.brushSize)

        """
        Adds the buttons to the layout which is added to the parent box.
        """
        qv = QVBoxLayout()
        qv.addWidget(self.brush_thickness)
        qv.addWidget(self.brushSizeLabel)
        self.groupBoxSlider.setLayout(qv)

        self.box.vbox.addWidget(self.groupBoxSlider)

    """
    thay đổi giá trị dựa trên slider
    """
    def sizeSliderChange(self, value):
        self.imageArea.brushSize = value
        self.brushSizeLabel.setText("%s px" % value)    
    
    """
    Tạo layout để chứa opacity slide
    """
    def setOpacitySlider(self):
        self.groupBoxSliderx = QGroupBox("Opacity")
        self.groupBoxSliderx.setMaximumHeight(60)
        self.groupBoxSliderx.setMinimumHeight(50)

        """
        cài đặt giá trị 0->1 cho slide brush
        """
        self.opacity_thicknesss = QSlider(Qt.Horizontal)
        self.opacity_thicknesss.setMinimum(10)
        self.opacity_thicknesss.setMaximum(100)
        self.opacity_thicknesss.setValue(100)
        self.opacity_thicknesss.valueChanged.connect(self.opacitySliderChange)

        """
        add widget to layout
        """
        qv = QVBoxLayout()
        qv.addWidget(self.opacity_thicknesss)
        self.groupBoxSliderx.setLayout(qv)
        self.box.vbox.addWidget(self.groupBoxSliderx)

    """
    thay đổi giá trị dựa trên slider
    """
    def opacitySliderChange(self, value):
        newValue = value * 0.01
        self.imageArea.opacity = newValue
        self.imageArea.opacityDrawZone(value)


    """
    tạo layout cho vùng color
    """
    def setColorChanger(self):
        self.groupBoxColor = QGroupBox("Color")
        self.groupBoxColor.setMaximumHeight(100)
        self.groupBoxColor.setMaximumHeight(100)

        """
        tạo color và cài đặt cho button với màu color này
        """
        self.col = QColor(0, 0, 0)
        self.brush_colour = QPushButton()
        self.brush_colour.setFixedSize(60, 60)
        self.brush_colour.clicked.connect(self.showColorDialog)
        
        self.brush_colour.setStyleSheet("background-color: %s" % self.col.name())
        self.box.vbox.addWidget(self.brush_colour)

        """
        add widget to layout
        """
        qv = QVBoxLayout()
        qv.addWidget(self.brush_colour)
        self.groupBoxColor.setLayout(qv)

        self.box.vbox.addWidget(self.groupBoxColor)

    """
    hiện thị color pick
    """
    def showColorDialog(self):
        self.col = QColorDialog.getColor()
        if self.col.isValid():
            self.brush_colour.setStyleSheet("background-color: %s" % self.col.name())
            self.imageArea.brushColor = self.col
        
        

    """
    scale img với new size
    """
    def resizeEvent(self, a0: QResizeEvent):
        if self.imageArea.resizeSavedImage.width() != 0:
            self.imageArea.image = self.imageArea.resizeSavedImage.scaled(self.imageArea.width(), self.imageArea.height(), Qt.IgnoreAspectRatio)
        self.imageArea.update()


    """
    mở file ra và save lại ở nơi mình muốn
    """
    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":
            return
        self.imageArea.image.save(filePath)

    """
    open file từ device để load lên
    """
    def open(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":
            return
        with open(filePath, 'rb') as f:
            content = f.read()
            self.imageArea.currentImg = filePath

        """
        load data file cho vùng img và update khi nó được scale 
        """
        self.imageArea.image.loadFromData(content)
        self.imageArea.image = self.imageArea.image.scaled(self.imageArea.width(), self.imageArea.height(), Qt.IgnoreAspectRatio)
        self.imageArea.resizeSavedImage = self.imageArea.image  # saves the image for later resizing
        self.imageArea.update()

    """
    quay trở lại state img trước đó
    """
    def undo(self):
        copyImage = self.imageArea.image
        if self.imageArea.savedImage.width() != 0:
            """
            khi có saveimage setup image lại cho nó scale ra đúng kích thước 
            """
            self.imageArea.image = self.imageArea.savedImage.scaled(self.imageArea.width(), self.imageArea.height(), Qt.IgnoreAspectRatio)
        else:
            """
            ko có state nào được lưu thì chỉ cần clear cái hiện tại
            """
            self.imageArea.image = QImage(self.imageArea.width(), self.imageArea.height(), QImage.Format_RGB32)
            self.imageArea.image.fill(Qt.white)
        """
        gán copyimge cho save khi undo
        """
        self.imageArea.savedImage = copyImage
        self.imageArea.update()

    """
    CLEAR và update lại DrawArea
    """
    def clear(self):
        self.imageArea.image.load(self.imageArea.currentImg)
        self.imageArea.resizeSavedImage = self.imageArea.image
        self.imageArea.image = self.imageArea.resizeSavedImage.scaled(self.imageArea.width(), self.imageArea.height(), Qt.IgnoreAspectRatio)
        self.imageArea.update()

    """
    EXIT PROGRAM
    """
    def exitProgram(self):
        QCoreApplication.quit()

    """
    ABOUT 
    """
    def about(self):
        self.msg.setWindowTitle("Info")
        self.msg.setText("""This Tool supports Cinematic Layout 
If you have any problem please contact me: thinh.nguyen_a """)
        self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.msg.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
