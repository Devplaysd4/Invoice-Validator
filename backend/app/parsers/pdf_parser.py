import pdfplumber
import re
from app.utils.field_extractor import (
    find_invoice_number,
    find_invoice_date,
    find_amount,
    find_vendor,
)

def extract_pdf_text(file_path: str):

    extracted_text = ""

    with pdfplumber.open(file_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                extracted_text += page_text + "\n"

    return extracted_text


def find_invoice_number(text: str):

    patterns = [

        r"Invoice Number[:\s]+([A-Za-z0-9\-\/]+)",

        r"Invoice No[:\s]+([A-Za-z0-9\-\/]+)",

        r"Invoice #[:\s]+([A-Za-z0-9\-\/]+)",

        r"Inv Number[:\s]+([A-Za-z0-9\-\/]+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1)

    return None


def find_invoice_date(text: str):

    patterns = [

        r"Invoice Date[:\s]+([0-9]{4}-[0-9]{2}-[0-9]{2})",

        r"Invoice Date[:\s]+([0-9]{2}/[0-9]{2}/[0-9]{4})",

        r"Date[:\s]+([0-9]{4}-[0-9]{2}-[0-9]{2})",

        r"Date[:\s]+([0-9]{2}/[0-9]{2}/[0-9]{4})"
    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1)

    return None


def find_amount(text: str):

    patterns = [

        r"Amount[:\s₹]*([0-9,.]+)",

        r"Total[:\s₹]*([0-9,.]+)",

        r"Grand Total[:\s₹]*([0-9,.]+)",

        r"Invoice Amount[:\s₹]*([0-9,.]+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:

            value = match.group(1).replace(",", "")

            try:
                return float(value)
            except:
                pass

    return None


def find_vendor(text: str):

    for line in text.splitlines():

        line = line.strip()

        if line:

            return line

    return None


def parse_pdf_file(file_path: str):

    text = extract_pdf_text(file_path)

    invoice = {

        "invoice_number": find_invoice_number(text),

        "vendor": find_vendor(text),

        "invoice_date": find_invoice_date(text),

        "amount": find_amount(text),

        "status": "PENDING",

        "validation_errors": None
    }

    return [invoice]