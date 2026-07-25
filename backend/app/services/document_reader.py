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

    # Upscale
    image = cv2.resize(
        image,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Remove noise
    gray = cv2.fastNlMeansDenoising(gray)

    # Sharpen
    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])

    gray = cv2.filter2D(
        gray,
        -1,
        kernel
    )

    # Binary threshold
    image = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    return image


# ----------------------------------
# OCR Helper
# ----------------------------------

def ocr_image(image):

    results = reader.readtext(
        image,
        detail=0,
        paragraph=True
    )

    return "\n".join(results)


# ----------------------------------
# Image Reader
# ----------------------------------

def read_image_text(image_path):

    image = cv2.imread(image_path)

    if image is None:
        raise Exception(
            f"Unable to read image: {image_path}"
        )

    image = preprocess_image(image)

    return ocr_image(image)


# ----------------------------------
# Text PDF
# ----------------------------------

def read_pdf_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

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