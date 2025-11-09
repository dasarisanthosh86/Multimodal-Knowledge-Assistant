import pytesseract
from PIL import Image
import os

# ✅ Path to your local Tesseract installation
# Make sure this matches your system path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_from_image(file_path, lang="eng"):
    """
    Extracts text from an image using Tesseract OCR.
    
    Args:
        file_path (str): Path to the image file.
        lang (str): Language code for OCR (default: English).

    Returns:
        str: Extracted text or an empty string if extraction fails.
    """
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return ""

    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang=lang)
        return text.strip()
    except Exception as e:
        print(f"❌ Failed to extract text from image: {e}")
        return ""
