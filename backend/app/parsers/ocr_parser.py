import cv2
import easyocr

from app.utils.field_extractor import (
    find_invoice_number,
    find_invoice_date,
    find_amount,
    find_vendor,
)

text = read_image_text(path)

invoice = extract_invoice(text)

return [invoice]

text = read_scanned_pdf(path)

invoice = extract_invoice(text)

return [invoice]