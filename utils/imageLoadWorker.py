from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage
from image_processing import load_image_file, load_image_url

class ImageLoadThread(QThread):
    Loaded = pyqtSignal(str, "PyQt_PyObject")

    def __init__(self, file_path, get_type='file'):
        QThread.__init__(self)
        self.cond = None
        self.mutex = None
        self._status = True
        self.kill = False
        self.filePath = file_path
        self.getType = get_type

    def __del__(self):
        self.wait()

    def run(self):
        try:
            if self.getType == 'file':
                image = load_image_file(self.filePath, return_type='qimage')
            elif self.getType == 'url':
                image = load_image_url(self.filePath, return_type='qimage')

            self.Loaded.emit(self.filePath, image)
        except:
            self.Loaded.emit(self.filePath, QImage())

    def toggle_status(self):
        self._status = not self._status
        if self._status:
            self.cond.wakeAll()

    @property
    def status(self):
        return self._status

    def stop(self):
        self.kill = True

    def setError(self):
        self.error = True

    def getError(self):
        return self.error