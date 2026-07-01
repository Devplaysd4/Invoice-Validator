import pandas as pd


def excel_to_dataframe(file_path):
    try:
        excel_data = pd.read_excel(file_path)

        print("Excel loaded successfully!\n")
        print (excel_data.to_string)
        print("First 5 Rows:")
        print(excel_data.head())

        print("\nColumns:")
        print(excel_data.columns.tolist())

        print(f"\nTotal Rows: {len(excel_data)}")

        return excel_data

    except Exception as error:
        print(f"Error: {error}")
        return None


if __name__ == "__main__":
    excel_data = excel_to_dataframe(
        "/home/deadpool/Projects/Invoice-Validator/data points/E_D_Bill_list_May2026_SAMPLE.xlsx"    )



    import pdfplumber

pdf_path = "data/sample_invoice.pdf"

with pdfplumber.open(pdf_path) as pdf:

    first_page = pdf.pages[0]

    text = first_page.extract_text()

    print(text)