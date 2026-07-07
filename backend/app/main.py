from fastapi import FastAPI

from app.database.database import Base,engine
from app.models.invoice import Invoice

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")

def root():
        return {"message": "Invoice Processor API Running"}