import pandas as pd


def parse_excel_file(file_path: str):
    df = pd.read_excel(file_path)

    records = df.to_dict(orient="records")

    return records