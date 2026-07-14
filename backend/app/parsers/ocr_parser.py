import cv2
import easyocr

from app.utils.field_extractor import (
    find_invoice_number,
    find_invoice_date,
    find_amount,
    find_vendor,
)

reader = easyocr.Reader(["en"], gpu=False)


def preprocess_image(image_path: str):
    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    threshold = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )[1]

    return threshold


def extract_text(image):
    results = reader.readtext(image)

    text = ""

    for result in results:
        text += result[1] + "\n"

    return text


def parse_image_file(file_path: str):
    processed = preprocess_image(file_path)

    text = extract_text(processed)

    invoice = {
        "invoice_number": find_invoice_number(text),
        "vendor": find_vendor(text),
        "invoice_date": find_invoice_date(text),
        "amount": find_amount(text),
        "status": "PENDING",
        "validation_errors": None,
    }

    return [invoice]