from app.validators.invoice_validator import validate_invoice

invoice = {
    "invoice_number": "",
    "vendor": "Amazon",
    "invoice_date": "2035-01-01",
    "amount": -50,
    "status": "PENDING",
    "validation_errors": None,
}

result = validate_invoice(invoice)

print(result)