import re
import pandas as pd

# Canonical names used throughout the project
COLUMN_ALIASES = {
    "invoice_number": [
        "invoice number",
        "invoice no",
        "invoice #",
        "invoice",
        "bill number",
        "bill no",
        "document number",
        "reference number",
        "inv number",
    ],
    "vendor": [
        "vendor",
        "supplier",
        "seller",
        "company",
        "customer",
        "employee name",
        "employee",
    ],
    "invoice_date": [
        "invoice date",
        "bill date",
        "date",
        "posting date",
        "from date",
    ],
    "amount": [
        "amount",
        "invoice amount",
        "grand total",
        "net amount",
        "total",
        "total payable",
        "total amount",
    ],
    "telephone_number": [
    "telephone_number",
    "telephone",
    "mobile",
    "mobile_number"
],

"account_number": [
    "account_number",
    "account"
],

"from_date": [
    "from_date"
],

"to_date": [
    "to_date"
],

"fixed_rent_charges": [
    "fixed_rent_charges"
],

"total": [
    "total"
],
}


def clean_column_name(value):
    """
    Convert any Excel header into a normalized form.
    Example:
        Invoice No. -> invoice_no
        Bill Number -> invoice_number
    """

    if value is None:
        return ""

    text = str(value).strip().lower()

    text = text.replace("\n", " ")
    text = text.replace("\r", " ")

    text = re.sub(r"[^a-z0-9_ ]", "", text)
    text = re.sub(r"\s+", " ", text)

    # Convert aliases to standard names
    for standard, aliases in COLUMN_ALIASES.items():
        if text in aliases:
            return standard

    return text.replace(" ", "_")


def detect_header_row(df):
    """
    Finds the row most likely to contain headers.
    Scores rows based on number of known invoice columns.
    """

    best_row = 0
    best_score = -1

    max_rows = min(25, len(df))

    for row in range(max_rows):

        score = 0

        for cell in df.iloc[row]:

            cleaned = clean_column_name(cell)

            if cleaned in COLUMN_ALIASES:
                score += 10

            elif cleaned != "":
                score += 1

        if score > best_score:
            best_score = score
            best_row = row

    return best_row


def make_unique(headers):
    """
    Duplicate column names become

    amount
    amount_2
    amount_3
    """

    seen = {}
    output = []

    for h in headers:

        if h == "":
            h = "unnamed"

        if h not in seen:

            seen[h] = 1
            output.append(h)

        else:

            seen[h] += 1
            output.append(f"{h}_{seen[h]}")

    return output


def remove_empty_columns(df):
    """
    Drops columns that are completely empty.
    """

    keep = []

    for column in df.columns:

        if not df[column].isna().all():
            keep.append(column)

    return df[keep]


def parse_excel_file(file_path):
    """
    Reads almost any invoice Excel into
    List[dict]
    """

    df = pd.read_excel(
        file_path,
        header=None,
        engine="openpyxl"
    )

    # merged cells support
    df = df.ffill()

    # remove fully empty rows
    df = df.dropna(how="all")

    # reset index
    df = df.reset_index(drop=True)

    header_row = None

    for i in range(len(df)):

        row = [str(x).strip().lower() for x in df.iloc[i].fillna("")]

        joined = " ".join(row)

        if (
            "telephone" in joined
            and "account" in joined
            and "invoice" in joined
    ):
            header_row = i
            break

    if header_row is None:
        header_row = detect_header_row(df)







    print("=" * 60)
    print("Detected Header Row:", header_row)
    print("=" * 60)

    headers = []

    for value in df.iloc[header_row]:
        headers.append(clean_column_name(value))

    headers = make_unique(headers)

    data = df.iloc[header_row + 1:].copy()

    data.columns = headers

    data = remove_empty_columns(data)

    data = data.dropna(how="all")

    data = data.where(pd.notnull(data), None)

    records = data.to_dict(orient="records")

    filtered_records = []

    for row in records:

    # Stop when footer starts
        if str(row.get("telephone_number", "")).strip().lower() == "total":
            break

    # Skip completely empty rows
        if not row.get("invoice_number"):
            continue

        filtered_records.append(row)

    print("\nHeaders:")
    print(headers)

    print("\nLAST RECORDS")
    from pprint import pprint
    pprint(filtered_records)

    return filtered_records