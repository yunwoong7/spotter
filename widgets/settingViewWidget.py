import os
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from config import get_config

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
        self.currentDetector = 'None'
        self.currentOcrEngine = 'Tesseract'


    def _loadUiInit(self):
        '''
        UI 초기화
        :return: None
        '''
        pass


    def _setEvent(self):
        '''
        event 설정
        :return: None
        '''
        self.cb_detector.currentIndexChanged['QString'].connect(self._cbDetectorCurrentIndexChanged)
        self.cb_ocrEngine.currentIndexChanged['QString'].connect(self._cbOcrEngineCurrentIndexChanged)


    def _cbDetectorCurrentIndexChanged(self, value):
        '''
        Detector Combo 변경 이벤트
        :param value: (str)
        :return: None
        '''
        self._config = get_config()

        if value in self._config["detection_function"]:
            self.currentDetector = value
        else:
            QMessageBox.information(self, "Select Detector", "현재 지원하지 않습니다.\n({})".format(value))
            lastitem_idx = self.cb_detector.findText(self.currentDetector)
            self.cb_detector.setCurrentIndex(lastitem_idx)


    def _cbOcrEngineCurrentIndexChanged(self, value):
        '''
        OCR Engine Combo 변경 이벤트
        :param value: (str)
        :return: None
        '''
        self._config = get_config()

        if value in self._config["ocr_engine"]:
            self.currentOcrEngine = value
        else:
            QMessageBox.information(self, "Select OCR Engine", "현재 지원하지 않습니다.\n({})".format(value))
            lastitem_idx = self.cb_ocrEngine.findText(self.currentOcrEngine)
            self.cb_ocrEngine.setCurrentIndex(lastitem_idx)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    canvas = SettingViewWidget()
    canvas.show()
    exit(app.exec_())