from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.invoice_routes import router as invoice_router
from app.api.upload_routes import router as upload_router

from app.database.database import Base, engine

# Import models so SQLAlchemy registers them
from app.models.invoice import Invoice

# Create FastAPI app FIRST
app = FastAPI(
    title="Intelligent Invoice Processing API"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(upload_router)
app.include_router(invoice_router)


@app.get("/")
def root():

    return {
        "message": "Invoice Processor API Running"
    }