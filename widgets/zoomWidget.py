import os
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QToolButton, QSlider
from PyQt5.QtCore import Qt

parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
widget_class = uic.loadUiType(os.path.join(parentDir, "UI/zoom_widget.ui"))[0]

class ZoomWidget(QWidget, widget_class):
    def __init__(self, value=100):
        super(ZoomWidget, self).__init__()
        self.setupUi(self)
        # self.sp_zoom.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.sp_zoom.setValue(value)

        # 모든 QToolButton을 투명하게 변경
        action_list = self.findChildren(QToolButton)
        slider_list = self.findChildren(QSlider)

        self.setAttribute(Qt.WA_TranslucentBackground)

        for item in action_list:
           item.setStyleSheet("background-color: rgba(0,0,0,0%)")

        for item in slider_list:
            item.setStyleSheet("QSlider::add-page:horizontal{background:#666;} QSlider{background: #455364;}")
