import os
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from widgets import SettingViewWidget, ResultViewWidget
import qdarkstyle

parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
widget_class = uic.loadUiType(os.path.join(parentDir, "UI/tab_widget.ui"))[0]

class TabWidget(QMainWindow, widget_class):
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
        self.result_view_widget = ResultViewWidget()

        self.lw_commonEffectList = self.setting_view_widget.lw_commonEffectList
        self.lw_eachEffectList = self.setting_view_widget.lw_eachEffectList

        self.layoutSettingView.addWidget(self.setting_view_widget)
        self.layoutResultView.addWidget(self.result_view_widget)

    def _setEvent(self):
        '''
        event 설정
        :return: None
        '''
        pass
        
    
    def setCurrentIndex(self, index):
        '''
        현재 Tab 변경
        :param index: (int)
        :return: None
        '''
        self.tab_main.setCurrentIndex(index)


    def getOcrMethod(self):
        '''
        Setting View Widget의 OCR Method를 Return
        :return: (str)
        '''
        return self.setting_view_widget.cb_ocrEngine.currentText()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    canvas = TabWidget()
    canvas.show()
    exit(app.exec_())