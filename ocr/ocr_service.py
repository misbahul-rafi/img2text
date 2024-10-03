import pytesseract
from .preprocess import preprocess_image

def convert_image_to_text(image_path):
    processed_image = preprocess_image(image_path)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config)
    return text