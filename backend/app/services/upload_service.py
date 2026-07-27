import os
import math
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

def clean_nan(obj):

    if isinstance(obj, dict):

        return {
            k: clean_nan(v)
            for k, v in obj.items()
        }

    if isinstance(obj, list):

        return [
            clean_nan(v)
            for v in obj
        ]

    if isinstance(obj, float):

        if math.isnan(obj):
            return None

    return obj

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
        "document_number",
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
    "company",
    "company_name",
    "customer",
    "organization",
    "organisation",
    "vendor_name",
    "provider",
    "service_provider"

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


import math

import pandas as pd

def get_value(row, aliases):

    for alias in aliases:

        value = row.get(alias)

        if pd.isna(value):
            continue

        if isinstance(value, str):

            value = value.strip()

            if value == "":
                continue

        return value

    return None

def normalize_invoice_row(row: dict):

    # -----------------------------------
    # Airtel Excel Format
    # -----------------------------------

    if "telephone_number" in row:

        return {

            "invoice_number": row.get("invoice_number"),

            "vendor": "Bharti Airtel",

            "invoice_date": row.get("from_date"),

            "amount": row.get("total_payable"),

            "fixed_rent": row.get("fixed_rent_charges"),

            "call_usage": row.get("call_usage_charges"),

            "adjustments": row.get("adjustments"),

            "cgst": row.get("cgst"),

            "sgst": row.get("sgst"),

            "discount": row.get("20_disc"),

            "status": "PENDING",

            "validation_errors": None

        }

    # -----------------------------------
    # Generic Vendor Detection
    # -----------------------------------

    vendor = get_value(row, COLUMN_ALIASES["vendor"])

    if vendor is None:

        for key, value in row.items():

            key_lower = str(key).lower()

            if any(word in key_lower for word in [

                "vendor",
                "company",
                "supplier",
                "organization",
                "organisation",
                "provider",
                "seller"

            ]):

                if value is not None and not pd.isna(value):

                    vendor = value
                    break

    # -----------------------------------
    # Generic Invoice
    # -----------------------------------

    return {

        "invoice_number": get_value(
            row,
            COLUMN_ALIASES["invoice_number"]
        ),

        "vendor": vendor,

        "invoice_date": get_value(
            row,
            COLUMN_ALIASES["invoice_date"]
        ),

        "amount": get_value(
            row,
            COLUMN_ALIASES["amount"]
        ),

        "fixed_rent": get_value(
            row,
            ["fixed_rent_charges", "fixed_rent"]
        ),

        "call_usage": get_value(
            row,
            ["call_usage_charges", "call_usage"]
        ),

        "adjustments": get_value(
            row,
            ["adjustments"]
        ),

        "cgst": get_value(
            row,
            ["cgst"]
        ),

        "sgst": get_value(
            row,
            ["sgst"]
        ),

        "discount": get_value(
            row,
            ["20_disc", "discount"]
        ),

        "status": "PENDING",

        "validation_errors": None

    }

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
            from pprint import pprint

            print("\nNORMALIZED TYPES")
            for row in normalized_rows:
                pprint(row)
                print(type(row["vendor"]))

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

        parsed_rows = clean_nan(parsed_rows)

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