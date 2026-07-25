import re
from datetime import datetime


# -----------------------------
# Utility
# -----------------------------

def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    return text.strip()


# -----------------------------
# Invoice Number
# -----------------------------

def find_invoice_number(text: str):

    patterns = [

        r"(?:Invoice\s*Number|Invoice\s*No\.?|Invoice\s*#|Inv\s*No\.?|Bill\s*Number|Bill\s*No\.?|Document\s*Number|Reference\s*Number)\s*[:\-]?\s*([A-Za-z0-9\-\/]+)",

        r"\bINV[- ]?[A-Za-z0-9]+\b",

        r"\bINVOICE[- ]?[A-Za-z0-9]+\b"

    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:

            return match.group(1).strip()

    return None


# -----------------------------
# Date
# -----------------------------

def normalize_date(date_string):

    if not date_string:
        return None

    formats = [

        "%d-%b-%Y",
        "%d %b %Y",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y-%m-%d",
        "%d.%m.%Y"

    ]

    for fmt in formats:

        try:

            return datetime.strptime(
                date_string.strip(),
                fmt
            ).strftime("%Y-%m-%d")

        except ValueError:

            pass

    return date_string


def find_invoice_date(text: str):

    patterns = [

        r"(?:Invoice\s*Date|Bill\s*Date|Date)\s*[:\-]?\s*([A-Za-z0-9\-\/ ]+)",

    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:

            return normalize_date(
                match.group(1)
            )

    return None


# -----------------------------
# Amount
# -----------------------------

def find_amount(text: str):

    patterns = [

        r"(?:Grand\s*Total|Net\s*Amount|Invoice\s*Amount|Total\s*Payable|Amount\s*Due|Total)\s*[:₹ ]*\s*([0-9,]+\.\d+)",

    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        if matches:

            try:

                value = matches[-1]

                return float(
                    value.replace(",", "")
                )

            except:

                pass

    return None


# -----------------------------
# Vendor
# -----------------------------

BAD_LINES = {

    "",

    "tax invoice",

    "invoice",

    "bill",

    "gst",

    "gstin",

    "pan",

    "hsn",

    "phone",

    "mobile",

    "email",

    "address",

    "quantity",

    "description",

    "amount"

}


def find_vendor(text: str):

    lines = clean_text(text).split("\n")

    for line in lines[:15]:

        candidate = line.strip()

        if len(candidate) < 3:
            continue

        lower = candidate.lower()

        skip = False

        for bad in BAD_LINES:

            if bad in lower:
                skip = True
                break

        if skip:
            continue

        if re.search(r"\d{6,}", candidate):
            continue

        return candidate

    return None


# -----------------------------
# Email
# -----------------------------

def find_email(text):

    match = re.search(

        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

        text

    )

    if match:

        return match.group(0)

    return None


# -----------------------------
# Phone
# -----------------------------

def find_phone(text):

    match = re.search(

        r"(?:\+91[- ]?)?[6-9]\d{9}",

        text

    )

    if match:

        return match.group(0)

    return None


# -----------------------------
# Final Extractor
# -----------------------------

def extract_invoice(text):

    text = clean_text(text)

    return {

        "invoice_number": find_invoice_number(text),

        "vendor": find_vendor(text),

        "invoice_date": find_invoice_date(text),

        "amount": find_amount(text),

        "email": find_email(text),

        "phone": find_phone(text),

        "status": "PENDING",

        "validation_errors": None

    }