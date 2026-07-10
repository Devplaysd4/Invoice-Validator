import os

from app.utils.file_handler import save_uploaded_file


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


def process_upload(file):
    saved_file_info = save_uploaded_file(file)

    file_type = detect_file_type(saved_file_info["original_filename"])

    return {
        "original_filename": saved_file_info["original_filename"],
        "saved_filename": saved_file_info["saved_filename"],
        "file_path": saved_file_info["file_path"],
        "file_size": saved_file_info["file_size"],
        "file_type": file_type
    }