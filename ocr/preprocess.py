import cv2

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast_image = clahe.apply(gray)
    final = cv2.medianBlur(contrast_image, 5)
    return final