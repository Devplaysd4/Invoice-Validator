import os

from app.parsers.csv_parser import parse_csv_file
from app.parsers.excel_parser import parse_excel_file
from app.parsers.pdf_parser import parse_pdf_file
from app.utils.file_handler import save_uploaded_file


def detect_file_type(filename: str):
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".csv":
        return "csv"
    elif extension in [".xlsx", ".xls"]:
        return "excel"
    elif extension == ".pdf":
        return "pdf"
    elif extension in [".png", ".jpg", ".jpeg"]:
        return "image"
    else:
        return "unsupported"


def normalize_invoice_row(row: dict):
    normalized_row = {
        "invoice_number": row.get("invoice_number")
        or row.get("Invoice Number")
        or row.get("Invoice No")
        or row.get("Inv Number")
        or row.get("invoice_no")
        or row.get("INVOICE_NUMBER"),

        "vendor": row.get("vendor")
        or row.get("Vendor")
        or row.get("Vendor Name")
        or row.get("Supplier"),

        "invoice_date": row.get("invoice_date")
        or row.get("Invoice Date")
        or row.get("Date"),

        "amount": row.get("amount")
        or row.get("Amount")
        or row.get("Total")
        or row.get("Invoice Amount"),

        "status": "PENDING",
        "validation_errors": None
    }

    return normalized_row


def normalize_invoice_rows(rows: list[dict]):
    normalized_rows = []

    for row in rows:
        normalized_rows.append(normalize_invoice_row(row))

    return normalized_rows


def process_upload(file):
    saved_file_info = save_uploaded_file(file)

    file_type = detect_file_type(saved_file_info["original_filename"])

    parsed_rows=[]

    if file_type == "csv":
        raw_rows = parse_csv_file(saved_file_info["file_path"])
        parsed_rows = normalize_invoice_rows(raw_rows)

    elif file_type == "excel":
        raw_rows = parse_excel_file(saved_file_info["file_path"])
        parsed_rows = normalize_invoice_rows(raw_rows)

    elif file_type == "pdf":

        raw_rows = parse_pdf_file(
            saved_file_info["file_path"]
    )

        parsed_rows = normalize_invoice_rows(raw_rows)

    return {
        "original_filename": saved_file_info["original_filename"],
        "saved_filename": saved_file_info["saved_filename"],
        "file_path": saved_file_info["file_path"],
        "file_size": saved_file_info["file_size"],
        "file_type": file_type,
        "parsed_rows":parsed_rows
    }