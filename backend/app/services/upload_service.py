import os

from app.parsers.csv_parser import parse_csv_file
from app.parsers.excel_parser import parse_excel_file
from app.services.document_reader import (
    read_pdf_text,
    read_image_text,
    read_scanned_pdf,
)

from app.services.field_extractor import extract_invoice
from app.utils.file_handler import save_uploaded_file


from app.validators.invoice_validator import validate_invoice
from app.validators.report_generator import generate_validation_report

from app.services.database_service import save_invoices

def process_rows(raw_rows):
    normalized = normalize_invoice_rows(raw_rows)
    return validate_invoice_rows(normalized)

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

COLUMN_ALIASES = {

    "invoice_number": [

        "invoice_number",
        "invoice_no",
        "invoice",
        "bill_number",
        "document_number"
        "invoicenumber",
        "INVOICE NO.",
        "INVOICE NUMBER",
        "INVOICE_NUMBER",
        "INVOICE_NO.",
        "INVOICE NO",
        "INVOICENO."
    ],

    "vendor": [

        "vendor",
        "supplier",
        "seller",
        "company"

    ],

    "invoice_date": [

        "invoice_date",
        "date",
        "bill_date",
        "from_date",
        "fromdate",
        "INVOICE DATE",
        "INVOICE_DATE",
        "BILL_DATE",
        "BILLDATE",
        "DATE"

    ],

    "amount": [

        "amount",
        "invoice_amount",
        "total",
        "total_payable",
        "grand_total",
        "net_amount",
        "AMOUNT",
        "TOTAL",
    ]

}


def get_value(row, aliases):

    for alias in aliases:

        value = row.get(alias)

        if value not in [None, "", "None"]:

            return value

    return None

def normalize_invoice_row(row: dict):

    # Airtel Excel
    if "invoicenumber" in row:

        return {

            "invoice_number": row.get("invoicenumber"),

            "vendor": "Bharti Airtel",

            "invoice_date": row.get("fromdate"),

            "amount": row.get("totalpayable"),

            "status": "PENDING",

            "validation_errors": None

        }

    # Generic invoices

    return {

        "invoice_number": get_value(
            row,
            COLUMN_ALIASES["invoice_number"]
        ),

        "vendor": (
            get_value(row, COLUMN_ALIASES["vendor"])
            or "Bharti Airtel"
),

        "invoice_date": get_value(
            row,
            COLUMN_ALIASES["invoice_date"]
        ),

        "amount": get_value(
            row,
            COLUMN_ALIASES["amount"]
        ),

        "status": "PENDING",

        "validation_errors": None

    }

    return normalized_row

def normalize_invoice_rows(rows: list[dict]):
    normalized_rows = []

    for row in rows:
        normalized_rows.append(normalize_invoice_row(row))

    return normalized_rows

def validate_invoice_rows(rows: list[dict]):

    validated_rows = []

    for row in rows:

        validated_rows.append(
            validate_invoice(row)
        )

    return validated_rows

def process_upload(file, db):

    saved_file_info = save_uploaded_file(file)

    file_type = detect_file_type(saved_file_info["original_filename"])

    print("Detected file type:", file_type)
    print("Saved path:", saved_file_info["file_path"])

    parsed_rows = []

    try:

        if file_type == "csv":

            raw_rows = parse_csv_file(
                saved_file_info["file_path"]
            )
            print("Total rows:", len(raw_rows))

            for row in raw_rows:
                print(
                    row.get("invoice_number"),
                    row.get("total_payable")
    )
            parsed_rows = process_rows(raw_rows)

        elif file_type == "excel":

            raw_rows = parse_excel_file(
                saved_file_info["file_path"]
)

# Airtel format detected
            if (
                len(raw_rows) > 0
                and "telephone_number" in raw_rows[0]
):
                print("Airtel Excel detected.")

            from pprint import pprint

            print("\n========== RAW ROWS ==========")
            pprint(raw_rows[:3])
            print("==============================")

            normalized_rows = normalize_invoice_rows(raw_rows)

            print("\n========== NORMALIZED ROWS ==========")
            pprint(normalized_rows[:3])
            print("=====================================")

            parsed_rows = validate_invoice_rows(
                normalized_rows
    )

            print("\n========== VALIDATED ROWS ==========")
            pprint(parsed_rows[:3])
            print("====================================")

        elif file_type == "pdf":

            from app.services.document_reader import read_document

            text = read_pdf_text(saved_file_info["file_path"])

            print("Embedded PDF text length:", len(text))

            if len(text.strip()) < 100:

                print("Using OCR...")

                text = read_scanned_pdf(
                    saved_file_info["file_path"]
    )

            print(text[:1000])

            invoice = extract_invoice(text)

            parsed_rows = process_rows([invoice])

        elif file_type == "image":

            text = read_image_text(
                saved_file_info["file_path"]
            )

            invoice = extract_invoice(text)

            parsed_rows = process_rows([invoice])

        else:

            raise ValueError("Unsupported file type.")

        report = generate_validation_report(parsed_rows)

        print("\n========== PARSED ROWS ==========")

        for row in parsed_rows:
            print(row)

        print("=================================\n")

        saved_invoices = save_invoices(
            db,
            parsed_rows
        )

        return {

            "original_filename": saved_file_info["original_filename"],

            "saved_filename": saved_file_info["saved_filename"],

            "file_path": saved_file_info["file_path"],

            "file_size": saved_file_info["file_size"],

            "file_type": file_type,

            "parsed_rows": parsed_rows,

            "validation_report": report,

            "database": {

                "saved_records": len(saved_invoices["saved"]),

                "saved_invoice_ids": [
                    invoice.id
                    for invoice in saved_invoices["saved"]
                ],

                "duplicates": saved_invoices["duplicates"]

            }

        }

    except Exception as e:

        import traceback

        traceback.print_exc()

        raise