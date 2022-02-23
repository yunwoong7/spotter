import uuid
from image_processing import convert_image, grayScale

class Effect(object):
    effect_data = {}
    def __init__(self, effect_type, option={}):
        self.id = str(uuid.uuid4())
        self.effect_type = effect_type
        self.effect_data['option'] = option

    def __setitem__(self, key, value):
        self.effect_data[key] = value

    def __getitem__(self, key):
        return self.effect_data[key]

    def getType(self):
        return self.effect_type

    def existOption(self):
        if self.effect_data['option'] == {}:
            return False
        else:
            return True

    def apply(self, img):
        cv_img = convert_image(img, 'cv2')

        if self.effect_type == 'Grayscale':
            result_img = grayScale(cv_img)

        result_img = convert_image(result_img, 'qimage')

        return result_img