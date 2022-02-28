import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow

import qdarkstyle

parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
widget_class = uic.loadUiType(os.path.join(parentDir, "UI/result_view_widget.ui"))[0]

class ResultViewWidget(QMainWindow, widget_class):

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
        pass


    def _setEvent(self):
        '''
        event 설정
        :return: None
        '''
        pass

    def setOcrResult(self, text):
        self.edt_ocrResult.setText(str(text))


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    canvas = ResultViewWidget()
    canvas.show()
    exit(app.exec_())