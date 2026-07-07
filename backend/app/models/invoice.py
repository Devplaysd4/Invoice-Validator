from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text
from datetime import datetime

from app.database.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, nullable=False)
    vendor = Column(String, nullable=False)
    invoice_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    validation_errors = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)