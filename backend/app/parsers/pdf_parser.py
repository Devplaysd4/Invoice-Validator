import pdfplumber
import re
from app.utils.field_extractor import (
    find_invoice_number,
    find_invoice_date,
    find_amount,
    find_vendor,
)

text = read_pdf_text(path)

invoice = extract_invoice(text)

return [invoice]