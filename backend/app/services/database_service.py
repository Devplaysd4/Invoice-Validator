from sqlalchemy.orm import Session

from app.models.invoice import Invoice

import json

def save_invoices(db: Session, invoices):

    saved = []
    duplicates = []
    seen = set()


    for invoice_data in invoices:

        invoice_number = invoice_data.get("invoice_number")
        import math

        if invoice_number is None:
            continue

        if isinstance(invoice_number, float) and math.isnan(invoice_number):
            continue

        invoice_number = str(invoice_number).strip()

        if invoice_number == "":
            continue

        if invoice_number in seen:

            duplicates.append({
                "invoice_number": invoice_number,
                "reason": "Duplicate in uploaded file"
        })

            continue

        seen.add(invoice_number)
        # Skip invalid invoices while parsing is being fixed
        if invoice_data["status"] == "INVALID":
            continue        
        existing = (
            db.query(Invoice)
            .filter(
                Invoice.invoice_number == invoice_number
            )
            .first()
        )

        if existing:

            duplicates.append({
                "invoice_number": invoice_number,
                "reason": "Already exists"
            })

            continue


        invoice = Invoice(

            invoice_number=invoice_data["invoice_number"],

            vendor=invoice_data["vendor"],

            invoice_date=invoice_data["invoice_date"],

            amount=invoice_data["amount"],

            status=invoice_data["status"],

            validation_errors=json.dumps(invoice_data["validation_errors"],indent=2)

        )

        db.add(invoice)

        saved.append(invoice)

    try:

        db.commit()

        for invoice in saved:
            db.refresh(invoice)

    except Exception:

        db.rollback()

        raise
    
    
    return {

        "saved": saved,

        "duplicates": duplicates

    }