import os
import math
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QProgressDialog, QSizePolicy, QApplication
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage, QImageReader
from widgets.zoomWidget import ZoomWidget
from utils.canvas import Canvas
from utils.imageLoadWorker import ImageLoadThread
import qdarkstyle
from config import get_config

__appname__ = 'Cavas View Widget'
parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
form_class = uic.loadUiType(os.path.join(parentDir, "UI/canvas_view_widget.ui"))[0]

class CanvasViewWidget(QMainWindow, form_class):
    Loaded = pyqtSignal(str, "PyQt_PyObject")
    Droped = pyqtSignal(str)

    FIT_WINDOW, FIT_WIDTH, MANUAL_ZOOM = 0, 1, 2

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._setting()
        self._loadUiInit()
        self._setEvent()
        self.dropLoad = True

        # self.loadImage('/Users/a06790/PycharmProjects/bizfarm_mvp_1/asset/images/test_image.jpg', get_type='file')
        # self.loadImage('https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FqIKfN%2FbtrqytiCGXP%2FDrlKqg7nZDNCrHTbosXhK0%2Fimg.jpg', get_type='url')


    def _setting(self):
        '''
        Setting
        :return: None
        '''
        self.org_image = QImage()
        self.image = QImage()
        self.filename = ''
        self._config = get_config()

        self.scroll_values = {Qt.Horizontal: {},
                              Qt.Vertical: {},
                              }
        self.zoom_values = {}
        self.zoomMode = self.FIT_WINDOW
        self.scalers = {self.FIT_WINDOW: self.scaleFitWindow,
                        self.FIT_WIDTH: self.scaleFitWidth,
                        # Set to one to scale to 100% when loading files.
                        self.MANUAL_ZOOM: lambda: 1,
                        }


    def _loadUiInit(self):
        '''
        UI 초기화
        :return: None
        '''
        # Zoom Widget
        self.zoomWidget = ZoomWidget()
        self.zoomWidget.setStyleSheet("background-color: rgba(0,0,0,30%)")
        self.view_toolbar.addWidget(self.zoomWidget)

        # Cavas Widget
        self.canvas = Canvas(
            epsilon=self._config["epsilon"],
            double_click=self._config["canvas"]["double_click"],
        )

        self.scrollArea.setWidget(self.canvas)
        self.scrollArea.setWidgetResizable(True)
        self.scrollBars = {
            Qt.Vertical: self.scrollArea.verticalScrollBar(),
            Qt.Horizontal: self.scrollArea.horizontalScrollBar(),
        }

        self.setAcceptDrops(True)


    def _setEvent(self):
        '''
        event 설정
        :return: None
        '''
        # Canvas
        self.canvas.scrollRequest.connect(self.scrollRequest)
        self.canvas.wheelEvent = self.canvasWheelEvent

        # Zoom
        self.zoomWidget.sp_zoom.valueChanged.connect(self.paintCanvas)
        self.zoomWidget.btn_zoomIn.clicked.connect(lambda: self.addZoom(increment=1.1))
        self.zoomWidget.btn_zoomOut.clicked.connect(lambda: self.addZoom(increment=0.9))
        self.zoomWidget.btn_fitWindow.clicked.connect(lambda: self.setFitWindow(value=True))
        self.zoomWidget.btn_fitWidth.clicked.connect(lambda: self.setFitWidth(value=True))
        self.zoomWidget.btn_originalSize.clicked.connect(lambda: self.setZoom(value=100))


    def dragEnterEvent(self, event):
        extensions = [
            ".%s" % fmt.data().decode().lower()
            for fmt in QImageReader.supportedImageFormats()
        ]
        if event.mimeData().hasUrls():
            items = [i.toLocalFile() for i in event.mimeData().urls()]
            if any([i.lower().endswith(tuple(extensions)) for i in items]):
                event.accept()
        else:
            event.ignore()


    def dropEvent(self, event):
        # if not self.mayContinue():
        #     event.ignore()
        #     return
        items = [i.toLocalFile() for i in event.mimeData().urls()]
        self.importDroppedImageFiles(items)


    def _initData(self):
        self.org_image = QImage()
        self.image = QImage()
        self.filename = ''
        self.canvas.resetState()

        # ==================================== Canvas ====================================

    def scrollRequest(self, delta, orientation):
        units = -delta * 0.1  # natural scroll
        bar = self.scrollBars[orientation]
        value = bar.value() + bar.singleStep() * units
        self.setScroll(orientation, value)


    def setScroll(self, orientation, value):
        self.scrollBars[orientation].setValue(int(value))
        self.scroll_values[orientation][self.filename] = value


    def setZoom(self, value):
        # self.actions.fitWidth.setChecked(False)
        # self.actions.fitWindow.setChecked(False)
        self.zoomMode = self.MANUAL_ZOOM
        self.zoomWidget.sp_zoom.setValue(value)
        self.zoom_values[self.filename] = (self.zoomMode, value)


    def addZoom(self, increment=1.1):
        if not self.image.isNull():
            zoom_value = self.zoomWidget.sp_zoom.value() * increment
            if increment > 1:
                zoom_value = math.ceil(zoom_value)
            else:
                zoom_value = math.floor(zoom_value)
            self.setZoom(zoom_value)


    def paintCanvas(self):
        # assert not self.image.isNull(), "cannot paint null image"
        if not self.image.isNull():
            self.canvas.scale = 0.01 * self.zoomWidget.sp_zoom.value()
            self.canvas.adjustSize()
            self.canvas.update()


    def adjustScale(self, initial=False):
        value = self.scalers[self.FIT_WINDOW if initial else self.zoomMode]()
        value = int(100 * value)
        self.zoomWidget.sp_zoom.setValue(value)
        self.zoom_values[self.filename] = (self.zoomMode, value)


    def scaleFitWindow(self):
        """Figure out the size of the pixmap to fit the main widget."""
        e = 90.0  # 스크롤바가 생성되지 않도록 설정
        w1 = self.width() - e
        h1 = self.height() - e
        a1 = w1 / h1

        # 종횡비를 기반으로 새로운 스케일 값을 계산
        w2 = self.canvas.pixmap.width() - 0.0
        h2 = self.canvas.pixmap.height() - 0.0
        a2 = w2 / h2

        return w1 / w2 if a2 >= a1 else h1 / h2


    def scaleFitWidth(self):
        e = 50.0 # 스크롤바가 생성되지 않도록 설정
        w = self.centralWidget().width() - e
        return w / self.canvas.pixmap.width()


    def setFitWindow(self, value=True):
        if not self.image.isNull():
            self.zoomMode = self.FIT_WINDOW if value else self.MANUAL_ZOOM
            self.adjustScale()


    def setFitWidth(self, value=True):
        if not self.image.isNull():
            self.zoomMode = self.FIT_WIDTH if value else self.MANUAL_ZOOM
            self.adjustScale()


    def canvasWheelEvent(self, QWheelEvent):
        '''
        Canvas Ctrl + Mouse Wheel (이미지 확대/축소)
        :param QWheelEvent: event
        :return: None
        '''
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            delta = QWheelEvent.angleDelta().y()

            if delta > 0:
                self.addZoom(increment=1.1)

            elif delta < 0:
                self.addZoom(increment=0.9)

    # ==================================== Image Load ====================================
    def getImage(self):
        '''
        Get Image
        :return: (PyQt5.QtGui.QImage)
        '''
        return self.image

    def getOrgImage(self):
        '''
        Get Original Image
        :return: (PyQt5.QtGui.QImage)
        '''
        return self.org_image


    def getFileName(self):
        '''
        Get File Name
        :return: (str)
        '''
        return self.filename


    def setAcceptDropLoad(self, bool):
        '''
        canvas view widget에 이미지를 Drag&Drop 할 경우 이미지를 Load 여부
        :param bool: (boolean) True
        :return: None
        '''
        self.dropLoad = bool


    def loadImage(self, filename=None, get_type='file'):
        self._initData()

        self.canvas.setEnabled(False)

        self._progress = QProgressDialog()
        self._progress.setLabelText('Loading...')
        self._progress.setRange(0, 0)
        self._progress.setCancelButton(None)
        self._progress.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._progress.setWindowFlag(Qt.FramelessWindowHint)
        self._progress.setModal(True)

        self.worker = ImageLoadThread(file_path=filename, get_type=get_type)
        self.worker.Loaded.connect(self.lodingComplete)
        self.worker.finished.connect(self.loadImageFinished)
        self._progress.show()
        self.worker.start()


    def lodingComplete(self, filename, image):
        self.org_image = image
        self.setImage(filename, image)
        self.paintCanvas()
        self.Loaded.emit(filename, image)


    def loadImageFinished(self):
        self.canvas.setEnabled(True)
        self._progress.hide()


    def setImage(self, filename, image):
        self.image = image

        if not self.image.isNull():
            self.filename = filename

            title = "{} - {}".format(__appname__, self.filename)
            self.setWindowTitle(title)

            self.canvas.loadPixmap(QPixmap.fromImage(self.image))

            is_initial_load = not self.zoom_values
            if self.filename in self.zoom_values:
                self.zoomMode = self.zoom_values[self.filename][0]
                self.setZoom(self.zoom_values[self.filename][1])
            elif is_initial_load or not self._config["keep_prev_scale"]:
                self.adjustScale(initial=True)

            for orientation in self.scroll_values:
                if self.filename in self.scroll_values[orientation]:
                    self.setScroll(orientation, self.scroll_values[orientation][self.filename])


    def importDroppedImageFiles(self, imageFiles):
        extensions = [
            ".%s" % fmt.data().decode().lower()
            for fmt in QImageReader.supportedImageFormats()
        ]

        self.filename = None
        for filename in imageFiles:
            if not filename.lower().endswith(tuple(extensions)):
                continue

            if self.dropLoad:
                self.loadImage(filename, get_type='file')

            self.Droped.emit(filename)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    canvas = CanvasViewWidget()
    canvas.show()
    exit(app.exec_())