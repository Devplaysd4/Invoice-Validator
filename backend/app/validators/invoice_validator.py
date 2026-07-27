import re
from datetime import datetime

import pandas as pd

def validate_invoice_number(invoice):

    invoice_number = invoice.get("invoice_number")

    if pd.isna(invoice_number):
        return {
            "field": "invoice_number",
            "problem": "Missing invoice number",
            "value_found": None,
            "expected": "Non-empty invoice number"
        }

    invoice_number = str(invoice_number).strip()

    if invoice_number == "":
        return {
            "field": "invoice_number",
            "problem": "Missing invoice number",
            "value_found": "",
            "expected": "Non-empty invoice number"
        }

    return None

    

def validate_vendor(invoice):

    vendor = invoice.get("vendor")

    if not vendor:
        return "Vendor is missing"

    return None

def validate_invoice_date(invoice):

    invoice_date = invoice.get("invoice_date")

    if not invoice_date:
        return "Invoice Date is missing"

    formats = [

        "%Y-%m-%d",

        "%d/%m/%Y",

        "%d-%m-%Y",

        "%d.%m.%Y", 

    ]

    parsed = None

    for fmt in formats:

        try:

            parsed = datetime.strptime(invoice_date, fmt)

            break

        except ValueError:

            pass

    if parsed is None:
        return "Invoice Date format is invalid"

    if parsed.date() > datetime.today().date():
        return "Invoice Date cannot be in the future"

    return None

def validate_amount(invoice):

    amount = invoice.get("amount")

    if amount is None:
        return "Amount is missing"

    try:

        amount = float(amount)

    except ValueError:

        return "Amount is invalid"

    if amount <= 0:
        return {
    "field": "amount",
    "problem": "Amount must be greater than zero",
    "value_found": amount,
    "expected": "A positive number"
}

    return None

def validate_email(invoice):

    email = invoice.get("email")

    if not email:
        return None

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    if not re.match(pattern, email):

        return "Email format is invalid"

    return None

def validate_quantity(invoice):

    quantity = invoice.get("quantity")

    if quantity is None:
        return None

    try:

        quantity = float(quantity)

    except ValueError:

        return "Quantity is invalid"

    if quantity <= 0:

        return "Quantity must be greater than zero"

    return None

def validate_invoice(invoice):

    errors = []

    validators = [

    validate_invoice_number,
    validate_vendor,
    validate_invoice_date,
    validate_amount,
    validate_invoice_total,
    validate_email,
    validate_quantity

]

    for validator in validators:

        error = validator(invoice)

        if error:

            errors.append(error)

    invoice["validation_errors"] = errors if errors else []

    if errors:

        invoice["status"] = "INVALID"

    else:

        invoice["status"] = "VALID"

    return invoice
# return improve of others done for amound and inv number

def validate_invoice_total(invoice):

    required = [
        "fixed_rent",
        "call_usage",
        "adjustments",
        "cgst",
        "sgst",
        "discount",
        "amount"
    ]

    if any(invoice.get(x) is None for x in required):
        return None

    expected = (
        float(invoice["fixed_rent"])
        + float(invoice["call_usage"])
        + float(invoice["adjustments"])
        + float(invoice["cgst"])
        + float(invoice["sgst"])
        + float(invoice["discount"])
    )

    actual = float(invoice["amount"])

    if abs(expected - actual) > 1:

        return {
            "field": "amount",
            "problem": "Invoice total mismatch",
            "expected_total": round(expected,2),
            "actual_total": actual,
            "difference": round(actual-expected,2)
        }

    return None