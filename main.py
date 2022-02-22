import os
import sys

from PyQt5 import uic
from PyQt5.QtGui import QImageReader
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolButton, QMenu, QFileDialog, QListWidgetItem
from widgets import ImageTabWidget
import qdarkstyle

__appname__ = 'MVP #1'
form_class = uic.loadUiType("UI/mvp_1_main.ui")[0]

class MVP1Main(QMainWindow, form_class):

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
        self.filename = ''


    def _loadUiInit(self):
        '''
        UI 초기화
        :return: None
        '''
        # Main Toolbar Button
        self.btn_openImg = QToolButton()
        self.btn_openImg.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        menu.addAction(self.action_openFile)
        menu.addAction(self.action_openFolder)
        menu.addSeparator()
        menu.addAction(self.action_getUrlImage)

        self.btn_openImg.setMenu(menu)
        self.btn_openImg.setDefaultAction(self.action_openFile)

        self.btn_save = QToolButton()
        self.btn_save.setPopupMode(QToolButton.MenuButtonPopup)
        menu = QMenu()
        menu.addAction(self.action_save)
        self.btn_save.setMenu(menu)
        self.btn_save.setDefaultAction(self.action_save)

        self.main_toolbar.addWidget(self.btn_openImg)
        self.main_toolbar.addWidget(self.btn_save)

        self.image_tab_widget = ImageTabWidget()
        self.layoutMain.addWidget(self.image_tab_widget)


    def _setEvent(self):
        '''
        event 설정
        :return: None
        '''
        # Action
        self.action_openFile.triggered.connect(self.openFile)

        # Image List
        self.lw_imgList.itemSelectionChanged.connect(self.imgSelectionChanged)


    def openFile(self):
        '''
        이미지 파일 열기
        :return: None
        '''
        path = os.path.dirname(str(self.filename)) if self.filename else "."
        formats = ["*.{}".format(fmt.data().decode()) for fmt in QImageReader.supportedImageFormats()]
        filters = "Image & Label files (%s)" % " ".join(formats)
        filename = QFileDialog.getOpenFileName(self, "%s - Choose Image or Label file" % __appname__, path, filters,)

        filename, _ = filename
        filename = str(filename)

        if filename:
            if filename in self.imageList:
                self.lw_imgList.setCurrentRow(self.imageList.index(filename))
            else:
                item = QListWidgetItem(filename)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                item.setData(Qt.UserRole, 'file')
                self.lw_imgList.addItem(item)
                self.lw_imgList.setCurrentRow(self.imageList.index(filename))


    def imgSelectionChanged(self):
        items = self.lw_imgList.selectedItems()
        if not items:
            return
        item = items[0]
        get_type = item.data(Qt.UserRole)
        currIndex = self.imageList.index(str(item.text()))
        if currIndex < len(self.imageList):
            filename = self.imageList[currIndex]
            if filename:
                self.image_tab_widget.openFile(filename, get_type)

    @property
    def imageList(self):
        lst = []
        for i in range(self.lw_imgList.count()):
            item = self.lw_imgList.item(i)
            lst.append(item.text())
        return lst


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    canvas = MVP1Main()
    canvas.show()
    exit(app.exec_())