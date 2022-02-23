import os
import sys
from PyQt5 import uic
from PyQt5.QtGui import QImageReader
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolButton, QMenu, QFileDialog, QListWidgetItem, QInputDialog
from widgets import TabWidget, CanvasViewWidget, EffectItemWidget
from utils import Effect

import qdarkstyle
from config import get_config

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
        self._config = get_config()
        self.filename = ''

        self.common_effect = []
        self.each_effect = []

        print(self._config["detection_function"])


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

        self.canvas_view_widget = CanvasViewWidget()
        self.canvas_view_widget.setAcceptDropLoad(False)
        self.layoutImage.addWidget(self.canvas_view_widget)

        self.tab_widget = TabWidget()
        self.lw_commonEffectList = self.tab_widget.lw_commonEffectList
        self.lw_eachEffectList = self.tab_widget.lw_eachEffectList
        self.layoutTab.addWidget(self.tab_widget)


    def _setEvent(self):
        '''
        event 설정
        :return: None
        '''
        # Action
        self.action_openFile.triggered.connect(self.openFile)
        self.action_openFolder.triggered.connect(self.openFolder)
        self.action_grayscale.triggered.connect(self.effectGrayscale)

        # Image List
        self.lw_imgList.itemSelectionChanged.connect(self.imgSelectionChanged)

        # Canvas View Widget
        self.canvas_view_widget.Droped.connect(self.cavasImageDroped)


    def openFile(self):
        '''
        이미지 파일 열기
            - 이미지 파일을 선택하면 경로를 이미지 리스트에 추가한 후 ListWidget의 Row를 해당 위치로 변경
            - 이미지를 불러오는 이벤트는 ListWidget의 Row가 변경되는 이벤트에서 수행
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


    def openFolder(self, dirpath=None):
        '''
        폴더 이미지 목록 불러오기
        :param dirpath: (str)
        :return:
        '''
        defaultOpenDirPath = dirpath if dirpath else "."
        # recent_dir = self.settingDialog.getRecentDir()
        recent_dir = ''

        if recent_dir and os.path.exists(recent_dir):
            defaultOpenDirPath = recent_dir
        else:
            defaultOpenDirPath = (os.path.dirname(self.filename) if self.filename else ".")

        targetDirPath = str(QFileDialog.getExistingDirectory(self, self.tr("%s - Open Directory") % __appname__,defaultOpenDirPath, QFileDialog.ShowDirsOnly|QFileDialog.DontResolveSymlinks,))
        self.importDirImages(targetDirPath)


    def importDirImages(self, dirpath, pattern=None):
        '''
        입력된 폴더 경로에서 이미지 파일 목록을 추출하여 Image List Widget에 추가
        :param dirpath: (str)
        :param pattern:
        :return: None
        '''
        # self.settingDialog.setDir("SETTING_RECENT_DIR", dirpath)
        self.filename = None

        # self.lw_imgList.clear()
        for filename in self.scanAllImages(dirpath):
            if pattern and pattern not in filename:
                continue

            item = QListWidgetItem(filename)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setData(Qt.UserRole, 'file')

            self.lw_imgList.addItem(item)
        self.lw_imgList.setCurrentRow(0)


    def scanAllImages(self, folderPath):
        '''
        폴더 경로에서 이미지 파일만 추출
        :param folderPath:
        :return: (list)
        '''
        extensions = [
            ".%s" % fmt.data().decode().lower()
            for fmt in QImageReader.supportedImageFormats()
        ]

        images = []
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                if file.lower().endswith(tuple(extensions)):
                    relativePath = os.path.join(root, file)
                    images.append(relativePath)
        images.sort(key=lambda x: x.lower())
        return images


    def imgSelectionChanged(self):
        '''
        Image List Widget Row 변경 이벤트
            - canvas widget에 이미지 불러오기
        :return: None
        '''
        items = self.lw_imgList.selectedItems()
        if not items:
            return
        item = items[0]
        get_type = item.data(Qt.UserRole)
        currIndex = self.imageList.index(str(item.text()))

        if currIndex < len(self.imageList):
            filename = self.imageList[currIndex]
            if filename:
                self.canvas_view_widget.loadImage(filename, get_type)


    def cavasImageDroped(self, filename):
        '''
        Canvas View Widget에 Drag&Drop으로 이미지가 추가되면 호출되는 이벤트
        :param filename: (str)
        :return: None
        '''
        if filename in self.imageList:
            self.lw_imgList.setCurrentRow(self.imageList.index(filename))
        else:
            item = QListWidgetItem(filename)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            item.setData(Qt.UserRole, 'file')
            self.lw_imgList.addItem(item)
            self.lw_imgList.setCurrentRow(self.imageList.index(filename))


    @property
    def imageList(self):
        lst = []
        for i in range(self.lw_imgList.count()):
            item = self.lw_imgList.item(i)
            lst.append(item.text())
        return lst


    # ================================= Effect =================================

    def effectGrayscale(self):
        effect_range_kor, ok = QInputDialog.getItem(self, 'Image Effect', "Grayscale 효과를 추가 하시겠습니까?", ['공통 적용', '선택 이미지 적용'], 0, False)

        if ok and effect_range_kor:
            if effect_range_kor == '공통 적용':
                effect_list = self.common_effect
            else:
                effect_list = self.each_effect

            grayscale_effect = Effect(effect_type='Grayscale')
            effect_list.append(grayscale_effect)
            self.setEffectListView()
            self.applyImgEffect()

            print(len(effect_list))


    def setEffectListView(self):
        '''
        Image Effect List View Setting
        :return: None
        '''
        self.lw_commonEffectList.clear()
        self.lw_eachEffectList.clear()

        for effect in self.common_effect:
            self.addEffectList(self.lw_commonEffectList, effect, 'common')

        for effect in self.each_effect:
            self.addEffectList(self.lw_eachEffectList, effect, 'each')

        self.tab_widget.setCurrentIndex(1)


    def addEffectList(self, list_widget, effect, effect_range):
        '''
        List에 Effect를 추가
        :param list_widget:
        :param effect:
        :param effect_range:
        :return: None
        '''
        effect_item_widget = EffectItemWidget(parent=self, effect=effect, effect_range=effect_range)

        item = QListWidgetItem()
        list_widget.addItem(item)
        list_widget.setItemWidget(item, effect_item_widget)
        item.setSizeHint(effect_item_widget.sizeHint())


    def removeEffect(self, effect, effect_range):
        '''
        List에 Effect를 삭제
        :param effect:
        :param effect_range:
        :return: None
        '''
        if effect_range == 'common':
            self.common_effect.remove(effect)
        else:
            self.each_effect.remove(effect)

        self.applyImgEffect()
        self.setEffectListView()


    def applyImgEffect(self):
        '''
        이미지 효과를 적용
        :return: None
        '''
        image = self.canvas_view_widget.getImage()
        filename = self.canvas_view_widget.getFileName()

        if not image.isNull():
            for effect in self.common_effect:
                image = effect.apply(image)

            for effect in self.each_effect:
                image = effect.apply(image)

        self.canvas_view_widget.setImage(filename, image)
            # self.canvas.loadPixmap(QPixmap.fromImage(image))
            # self.paintCanvas()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
    canvas = MVP1Main()
    canvas.show()
    exit(app.exec_())