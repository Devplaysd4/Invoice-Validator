from sqlalchemy.orm import Session

from app.models.invoice import Invoice


def save_invoices(db: Session, invoices):

    saved = []
    duplicates = []

    for invoice_data in invoices:

        existing = (
            db.query(Invoice)
            .filter(
                Invoice.invoice_number == invoice_data["invoice_number"]
            )
            .first()
        )

        if existing:

            duplicates.append({
                "invoice_number": invoice_data["invoice_number"],
                "reason": "Already exists"
            })

            continue

        invoice = Invoice(

            invoice_number=invoice_data["invoice_number"],

            vendor=invoice_data["vendor"],

            invoice_date=invoice_data["invoice_date"],

            amount=invoice_data["amount"],

            status=invoice_data["status"],

            validation_errors=invoice_data["validation_errors"]

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