import uuid
from image_processing import convert_image, grayScale, cannyScan, hedScan

class Effect(object):
    def __init__(self, effect_type, option={}):
        self.effect_data = {}
        self.id = str(uuid.uuid4())
        self.effect_type = effect_type
        self.effect_data['option'] = option

    def __setitem__(self, key, value):
        self.effect_data[key] = value

    def __getitem__(self, key):
        return self.effect_data[key]

    def getType(self):
        return self.effect_type

    def getOption(self, key):
        if self.existOption():
            return self.effect_data['option'][key]
        else:
            return ''

    def existOption(self):
        if self.effect_data['option'] == {}:
            return False
        else:
            return True

    def apply(self, img):
        result_img = convert_image(img, 'cv2')

        if self.effect_type == 'Grayscale':
            result_img = grayScale(result_img)
        elif self.effect_type == 'Scanned':
            if self.getOption('type') == 'canny':
                result_img = cannyScan(result_img, 500)
            elif self.getOption('type') == 'hed':
                result_img = hedScan(result_img, 500)

        result_img = convert_image(result_img, 'qimage')

        return result_img