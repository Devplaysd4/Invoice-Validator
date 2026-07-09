from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.invoice import Invoice

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/invoices")
def get_all_invoices(db: Session=Depends(get_db)):
    invoices =db.query(Invoice).all()
    return invoices

@router.post("/invoices")
def create_invoice(invoice_number: str,
    vendor: str,
    invoice_date:date,
    amount:float,
    status:str,
    validation_errors:Optional[str] = None,
    db:Session =Depends(get_db)
):
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