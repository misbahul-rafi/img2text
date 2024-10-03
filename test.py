import os
import cv2
import pytesseract
import concurrent.futures

def preprocess_image(image_path):
  image = cv2.imread(image_path)
  resized_image = cv2.resize(image, None, fx=3, fy=3, interpolation=cv2.INTER_NEAREST)
  gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
  contrast_image = clahe.apply(gray)
  final = cv2.medianBlur(contrast_image, 5)
  return final

def convert_image_to_text(image_path):
    print("Memproses gambar...")
    # Pra-proses gambar
    processed_image = preprocess_image(image_path)
    
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(processed_image, config=custom_config)
    return text
  
def process_images(image_paths):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(convert_image_to_text, image_paths))
    return results

if __name__ == "__main__":
    image_paths = ["light.png", "dark.png"]
    try:
      extracted_texts = process_images(image_paths)
      for text in extracted_texts:
          print(text)
    except ValueError as e:
        print(e)
