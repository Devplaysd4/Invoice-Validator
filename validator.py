import pandas as pd
from datetime import datetime 
# loads csv to see first few rows 
# invoices.csv is error free
invoice_data = pd.read_csv("sample_invoice.csv")
print(invoice_data)
# column names
print(invoice_data.columns.tolist())
#iterates for row number and row data
# for index,row in invoice_data.iterrows():
#     print(row["amount"])
def validate_date(date):
    try:
        datetime.strptime(date,"%Y-%m-%d")
        return True
    except ValueError:
        return False    

def validate_amount(amount):
    try:
        amount = float(amount)
        if amount <= 0:
            return False
        return True
    except ValueError:
        return False
def validate_qty(qty):
    try:
        qty = int(qty)
        if qty <=0:
            return False
        return True
    except ValueError:
        return False

def validate_email(email):
    if"@"in email and"." in email:
        return True
    return False


errors = []
for index, row in invoice_data.iterrows():

    if not validate_date(row["date"]):#invoice_date for bigger data
        errors.append(f"Row {index}: Invalid Date")

    if not validate_amount(row["amount"]):
        errors.append(f"Row {index}: Invalid Amount")

    # if not validate_qty(row["qty"]):
        # errors.append(f"Row {index}: Invalid Quantity")

    # if not validate_email(row["email"]):
        # errors.append(f"Row {index}: Invalid Email")


print("\nValidation Report")

if len(errors) == 0:
    print("No errors found.")
else:
    for error in errors:
        print(error)

print(f"\nTotal Errors: {len(errors)}")
print(f"total data rows: {len(invoice_data)}")