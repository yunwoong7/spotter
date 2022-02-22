import os
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from widgets import SettingViewWidget, imageViewWidget
import qdarkstyle

parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
widget_class = uic.loadUiType(os.path.join(parentDir, "UI/image_tab_widget.ui"))[0]

class ImageTabWidget(QMainWindow, widget_class):
    ImageChanged = pyqtSignal(str, "PyQt_PyObject")

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self._setting()
        self._loadUiInit()
        self._setEvent()

    def _setting(self):
        '''
        Setting
        :return: None
        '''
        pass

    def _loadUiInit(self):
        '''
        UI 초기화
        :return: None
        '''
        self.setting_view_widget = SettingViewWidget()
        self.image_view_widget = imageViewWidget()

        self.layoutSettingView.addWidget(self.setting_view_widget)
        self.layoutResultView.addWidget(self.image_view_widget)

    def _setEvent(self):
        '''
        event 설정
        :return: None
        '''
        self.setting_view_widget.SettingViewLoaded.connect(self._settingViewImageLoaded)
        self.image_view_widget.ImageViewLoaded.connect(self._imageViewImageLoaded)


    def _settingViewImageLoaded(self, filename, image):
        '''
        Setting View 이미지 변경 이벤트
        :param filename: (str)
        :param image: (qimage)
        :return: None
        '''
        self.image_view_widget.setImage(filename, image)
        self.ImageChanged.emit(filename, image)


    def _imageViewImageLoaded(self, filename, image):
        '''
        Imnage View 이미지 변경 이벤트
        :param filename: (str)
        :param image: (qimage)
        :return: None
        '''
        self.setting_view_widget.setImage(filename, image)
        self.ImageChanged.emit(filename, image)
        
    
    def openFile(self, filename, get_type='file'):
        '''
        이미지파일 열기
        :param filename: (str)
        :return: None
        '''
        self.image_view_widget.openFile(filename, get_type=get_type)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    canvas = ImageTabWidget()
    canvas.show()
    exit(app.exec_())