import os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

parentDir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
dig_class = uic.loadUiType(os.path.join(parentDir, "UI/effect_item_widget.ui"))[0]

class EffectItemWidget(QDialog, dig_class):

    def __init__(self, parent, effect, effect_range):
        super(EffectItemWidget, self).__init__(parent)
        self.setupUi(self)
        self.mainWidget = parent

        op_dtm = "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())

        self.effect = effect
        self.effect_type = effect.getType()
        self.effect_range = effect_range
        self._loadUiInit()
        self._setEvent()
        self.setWidget()


    def get(self, key, default=None):
        if key in self.effect_data:
            if self.effect_data[key] == '':
                return default
            else:
                return self.effect_data[key]
        return default


    def _loadUiInit(self):
        self.setStyleSheet("background-color: rgba(230,230,230,0%)")
        pass

    def _setEvent(self):
        self.btn_setting.clicked.connect(self.settingClicked)
        self.btn_close.clicked.connect(self.closeClicked)
        self.btn_show.clicked.connect(self.showClicked)


    def setWidget(self):
        self.lbl_effectType.setText("{}".format(self.effect_type))

        if self.effect_type == 'Grayscale':
            self.lbl_icon.setPixmap(QPixmap(':/effect/icon/' + 'grayscale.png'))
        elif self.effect_type == 'Scanned':
            self.lbl_icon.setPixmap(QPixmap(':/effect/icon/' + 'scan.png'))
        elif self.effect_type == 'Rotate':
            self.lbl_icon.setPixmap(QPixmap(':/effect/icon/' + 'rotate.png'))
        elif self.effect_type == 'Resize':
            self.lbl_icon.setPixmap(QPixmap(':/effect/icon/' + 'resize.png'))
        elif self.effect_type == 'Horizontal Flip':
            self.lbl_icon.setPixmap(QPixmap(':/effect/icon/' + 'flip-vertical.png'))
        elif self.effect_type == 'Vertical Flip':
            self.lbl_icon.setPixmap(QPixmap(':/effect/icon/' + 'flip-horizontal.png'))
        elif self.effect_type == 'Document verification':
            self.lbl_icon.setPixmap(QPixmap(':/icon/' + 'document.png'))

        # self.btn_setting.hide()
        if self.effect.existOption():
            pass
        else:
            self.btn_setting.hide()

    def showClicked(self):
        self.effect.setApplied(self.btn_show.isChecked())
        self.mainWidget.applyImgEffect()

    def closeClicked(self):
        reply = QMessageBox.question(self.mainWidget, 'Effect 삭제', "[{}] Effect를 삭제하시겠습니까?".format(self.effect_type), QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.mainWidget.removeEffect(self.effect, self.effect_range)


    def settingClicked(self):
        pass

    def getProjectType(self):
        return self.project_type

    def getProjectName(self):
        return self.project_name

    def getProject(self):
        return self.project