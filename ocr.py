from PIL import Image
import pytesseract


class OCR():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\LENOVO\Documents\GitHub\MindSight\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(Image.open(''), lang='eng+fil')