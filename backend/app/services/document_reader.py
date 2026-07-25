import cv2
import easyocr
import pdfplumber
import numpy as np

from pdf2image import convert_from_path


reader = easyocr.Reader(
    ["en"],
    gpu=False
)


# ----------------------------------
# Image Preprocessing
# ----------------------------------

def preprocess_image(image):

    image = cv2.resize(
        image,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.fastNlMeansDenoising(gray)

    gray = cv2.GaussianBlur(gray, (3,3), 0)

    gray = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    kernel = np.ones((2,2), np.uint8)

    gray = cv2.morphologyEx(
        gray,
        cv2.MORPH_CLOSE,
        kernel
    )

    return gray


# ----------------------------------
# OCR Helper
# ----------------------------------

def ocr_image(image):

    results = reader.readtext(
        image,
        paragraph=True,
        detail=0,
        width_ths=0.8,
        height_ths=0.8
    )

    text = "\n".join(results)

    print("\n========== OCR OUTPUT ==========\n")
    print(text)
    print("\n===============================\n")

    return text


# ----------------------------------
# Image Reader
# ----------------------------------

def read_image_text(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise Exception(f"Unable to read image: {image_path}")

    image = preprocess_image(image)

    text = ocr_image(image)

    print("\n========== OCR OUTPUT ==========\n")
    print(text)
    print("\n================================\n")

    return text


# ----------------------------------
# Text PDF
# ----------------------------------

def read_pdf_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text(
    x_tolerance=2,
    y_tolerance=2
)
            if page_text:

                text += page_text
                text += "\n"

    return text.strip()


# ----------------------------------
# OCR PDF
# ----------------------------------

def read_scanned_pdf(pdf_path):

    pages = convert_from_path(
        pdf_path,
        dpi=300
    )

    text = ""

    for page in pages:

        image = np.array(page)

        image = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2BGR
        )

        image = preprocess_image(image)

        text += ocr_image(image)

        text += "\n"

    return text.strip()


# ----------------------------------
# Smart Reader
# ----------------------------------

def read_document(file_path):

    text = read_pdf_text(file_path)

    if len(text) > 100:
        return text

    print("No embedded text found.")
    print("Switching to OCR...")

    return read_scanned_pdf(file_path)