from fastapi import APIRouter,UploadFile, File

from app.services.upload_service import process_upload
router = APIRouter()

@router.post("/upload-invoice")
def upload_invoice(file: UploadFile = File(...)):
    upload_result = process_upload(file)

    return {
        "message": "Invoice file uploaded successfully",
        "data": upload_result
    }