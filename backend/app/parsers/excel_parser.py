import pandas as pd
import re


def parse_excel_file(file_path):

    df = pd.read_excel(
        file_path,
        header=None,
        engine="openpyxl"
    )

    header_row = detect_header_row(df)

    print(f"Detected Header Row: {header_row}")

    # Build headers manually
    headers = []

    for value in df.iloc[header_row]:

        headers.append(
            clean_column_name(value)
        )

    # Everything below header
    data = df.iloc[header_row + 1:].copy()

    data.columns = headers

    data = data.dropna(how="all")

    data = data.where(
        pd.notnull(data),
        None
    )

    return data.to_dict(
        orient="records"
    )