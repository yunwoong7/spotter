from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal
from recognition import tesseract_ocr

class RecognitionThread(QThread):
    Completed = pyqtSignal(str)

    def __init__(self, image, method=''):
        QThread.__init__(self)
        self.cond = None
        self.mutex = None
        self._status = True
        self.kill = False
        self.image = image
        self.method = method

    def __del__(self):
        try:
            self.wait()
        except RuntimeError:
            pass

    def run(self):
        text = ""

        if self.method == 'Tesseract':
            text = tesseract_ocr(self.image)

        self.Completed.emit(text)


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