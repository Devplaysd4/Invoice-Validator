from datetime import date
from typing import Optional


from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.invoice import Invoice


from fastapi import APIRouter, Depends, HTTPException










router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.get("/")
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
def create_invoice(invoice_number: str,
    vendor: str,
    invoice_date:date,
    amount:float,
    status:str,
    validation_errors:Optional[str] = None,
    db:Session =Depends(get_db)):
    new_invoice = Invoice(
        invoice_number=invoice_number,
        vendor=vendor,
        invoice_date=invoice_date,
        amount=amount,
        status=status,
        validation_errors=validation_errors
    )
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    return new_invoice
    