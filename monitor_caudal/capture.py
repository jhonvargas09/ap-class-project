"""Captura de una región de pantalla y lectura del número (OCR) que muestra."""
import os
import re

import mss
import pytesseract
from PIL import Image, ImageOps

tesseract_cmd = os.environ.get("TESSERACT_CMD")
if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

NUMBER_RE = re.compile(r"[-+]?\d+(?:[.,]\d+)?")
OCR_CONFIG = "--psm 7 -c tessedit_char_whitelist=0123456789.,-"


def grab_region_image(region):
    """region: dict con left, top, width, height (coordenadas de pantalla)."""
    with mss.mss() as sct:
        shot = sct.grab(region)
        img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
    return img


def preprocess_for_ocr(img, scale=3):
    img = ImageOps.grayscale(img)
    img = img.resize((img.width * scale, img.height * scale), Image.LANCZOS)
    img = ImageOps.autocontrast(img)
    return img


def read_number_from_region(region):
    """Devuelve el número detectado en la región (float) o None si no se pudo leer."""
    img = preprocess_for_ocr(grab_region_image(region))
    text = pytesseract.image_to_string(img, config=OCR_CONFIG)
    match = NUMBER_RE.search(text)
    if not match:
        return None
    value_str = match.group().replace(",", ".")
    try:
        return float(value_str)
    except ValueError:
        return None
