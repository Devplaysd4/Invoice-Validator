from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.services.upload_service import process_upload

router = APIRouter()


@router.post("/upload-invoice")
def upload_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)):
    upload_result = process_upload(file, db)

    return {
        "message": "Invoice file uploaded successfully",
        "data": upload_result
    }