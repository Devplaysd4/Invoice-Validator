from datetime import date

from pydantic import BaseModel


class InvoiceSchema(BaseModel):

    invoice_number: str

    vendor: str

    invoice_date: date

    amount: float

    status: str

    validation_errors: str | None = None