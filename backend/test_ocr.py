from app.parsers.ocr_parser import parse_image_file

text = parse_image_file("uploads/1.png")

print("========== OCR OUTPUT ==========")
print(text)
