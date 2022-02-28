import cv2
import pytesseract
from image_processing import convert_image

def tesseract_ocr(image, options="--psm 4", lang="kor+eng"):
    org_image = convert_image(image, 'cv2')
    rgb_image = cv2.cvtColor(org_image, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb_image, config=options, lang=lang)
    return text