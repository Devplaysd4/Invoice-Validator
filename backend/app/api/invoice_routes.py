from datetime import date

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.invoice import Invoice

from app.schemas.invoice_schema import InvoiceSchema

from app.services.database_service import update_invoice


router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.get("")
def get_all_invoices(
    db: Session = Depends(get_db)):

    invoices = db.query(Invoice).all()

    return invoices

@router.get("/{invoice_id}")
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)):

    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .first()
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return invoice

@router.get("/search/{invoice_number}")
def search_invoice(
    invoice_number: str,
    db: Session = Depends(get_db)):

    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.invoice_number == invoice_number
        )
        .first()
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return invoice

@router.get("/status/{status}")
def invoices_by_status(
    status: str,
    db: Session = Depends(get_db)):

    invoices = (
        db.query(Invoice)
        .filter(
            Invoice.status == status.upper()
        )
        .all()
    )

    return invoices

@router.delete("/{invoice_id}")
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)):

    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .first()
    )

    if invoice is None:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    db.delete(invoice)

    db.commit()

    return {

        "message":"Invoice deleted"

    }



@router.post("")
def create_invoice(
    invoice: InvoiceSchema,
    db: Session = Depends(get_db)
):

    new_invoice = Invoice(
        **invoice.model_dump()
    )

    db.add(new_invoice)

    db.commit()

    db.refresh(new_invoice)

    return new_invoice
@router.put("/{invoice_id}")

def edit_invoice(
    

    invoice_id: int,

    invoice: InvoiceSchema,

    db: Session = Depends(get_db)):

    updated = update_invoice(

        db,

        invoice_id,

        invoice.model_dump()

    )

    if updated is None:

        raise HTTPException(

            status_code=404,

            detail="Invoice not found"

        )

    return updated




@router.post("/override")
def save_anyway(
    invoice: InvoiceSchema,
    db: Session = Depends(get_db)
):

    new_invoice = Invoice(

        invoice_number=invoice.invoice_number,

        vendor=invoice.vendor,

        invoice_date=invoice.invoice_date,

        amount=invoice.amount,

        status="OVERRIDDEN",

        validation_errors=invoice.validation_errors

    )

    db.add(new_invoice)

    db.commit()

    db.refresh(new_invoice)

    return new_invoice