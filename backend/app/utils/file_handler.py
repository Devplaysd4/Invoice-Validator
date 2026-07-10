import os
import shutil
import uuid

UPLOAD_DIR = "uploads"

def save_uploaded_file(file):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    original_filename = file.filename
    file_extension = os.path.splitext(original_filename)[1]

    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    return {
        "original_filename": original_filename,
        "saved_filename": unique_filename,
        "file_path": file_path,
        "file_size": file_size
    }