import pytesseract
from .preprocess import preprocess

def convert2image(image_path):
    processed_image = preprocess(image_path)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config)
    return text