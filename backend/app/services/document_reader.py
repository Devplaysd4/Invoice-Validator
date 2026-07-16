import cv2
import easyocr
import pdfplumber
from pdf2image import convert_from_path
import numpy as np

reader = easyocr.Reader(
    ["en"],
    gpu=False
)

def preprocess_image(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    blur = cv2.GaussianBlur(
        gray,
        (3,3),
        0
    )

    threshold = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY+cv2.THRESH_OTSU
    )[1]

    return threshold

def read_image_text(image_path):

    image = cv2.imread(image_path)

    image = preprocess_image(image)

    results = reader.readtext(image)

    text=""

    for result in results:

        text += result[1]

        text += "\n"

    return text

def read_pdf_text(pdf_path):

    text=""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text

                text += "\n"

    return text

def read_scanned_pdf(pdf_path):

    images = convert_from_path(pdf_path)

    text = ""

    for page in images:

        image = np.array(page)

        image = cv2.cvtColor(
            image,
            cv2.COLOR_RGB2BGR
        )

        image = preprocess_image(image)

        result = reader.readtext(image)

        for line in result:

            text += line[1]

            text += "\n"

    return text

