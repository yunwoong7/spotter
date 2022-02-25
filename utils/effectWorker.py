from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal

class EffectThread(QThread):
    Completed = pyqtSignal(str, "PyQt_PyObject")

    def __init__(self, image, filename='', common_effect=[], each_effect=[]):
        QThread.__init__(self)
        self.cond = None
        self.mutex = None
        self._status = True
        self.kill = False
        self.image = image
        self.filename = filename
        self.common_effect = common_effect
        self.each_effect = each_effect

    def __del__(self):
        try:
            self.wait()
        except RuntimeError:
            pass

    def run(self):
        if not self.image.isNull():
            for effect in self.common_effect:
                self.image = effect.apply(self.image)

            for effect in self.each_effect:
                self.image = effect.apply(self.image)

        self.Completed.emit(self.filename, self.image)


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