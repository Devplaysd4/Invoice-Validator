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
