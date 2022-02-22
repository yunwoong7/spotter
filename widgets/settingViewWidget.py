import os
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from widgets import CanvasViewWidget

import qdarkstyle

parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
widget_class = uic.loadUiType(os.path.join(parentDir, "UI/setting_view_widget.ui"))[0]

class SettingViewWidget(QMainWindow, widget_class):
    SettingViewLoaded = pyqtSignal(str, "PyQt_PyObject")

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
        self.canvas_view_widget = CanvasViewWidget()
        self.layoutSettingView.addWidget(self.canvas_view_widget)


    def _setEvent(self):
        '''
        event 설정
        :return: None
        '''
        self.canvas_view_widget.Loaded.connect(self.lodingComplete)


    def lodingComplete(self, filename, image):
        '''
        이미지로드 완료 후 호출되는 이벤트
        :param filename: (str)
        :param image: (qimage)
        :return: None
        '''
        print(filename)
        self.SettingViewLoaded.emit(filename, image)


    def setImage(self, filename, image):
        '''
        canvas view widget에 이미지 설정
        :param filename: (str)
        :param image: (qimage)
        :return: None
        '''
        self.canvas_view_widget.setImage(filename, image)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    canvas = SettingViewWidget()
    canvas.show()
    exit(app.exec_())