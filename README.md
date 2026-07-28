<div align="center">

# 📄 Intelligent Invoice Processing System

### Extract • Validate • Store • Manage

An end-to-end full-stack invoice processing platform that automates invoice extraction, validation, OCR, and database management using **FastAPI**, **React**, and **PostgreSQL**.

<img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi">
<img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react">
<img src="https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql">
<img src="https://img.shields.io/badge/OCR-EasyOCR%20%2B%20Tesseract-blueviolet?style=for-the-badge">
<img src="https://img.shields.io/badge/Python-3.12-yellow?style=for-the-badge&logo=python">

</div>

---

# 🎯 Why This Project?

Processing invoices manually is repetitive, slow, and prone to human error.

This project simulates how a modern enterprise invoice management system works by allowing users to upload invoices in different formats, automatically extracting information, validating business rules, storing records inside PostgreSQL, and managing everything through a clean dashboard.

Instead of manually entering invoice information, users simply upload the document—the system handles the rest.

---

# ⚡ Features

## 📤 Smart Upload

Supports

- CSV
- Excel
- PDF
- Images

with automatic file type detection.

---

## 🤖 Intelligent Extraction

Extracts invoice information such as

- Invoice Number
- Vendor
- Invoice Date
- Amount
- GST
- Discounts
- Charges

using

- pdfplumber
- EasyOCR
- Tesseract OCR

---

## ✅ Validation Engine

Every invoice is validated before entering the database.

Checks include

✔ Missing Invoice Numbers

✔ Missing Vendors

✔ Invalid Dates

✔ Future Dates

✔ Invalid Amounts

✔ Negative Values

✔ Duplicate Invoice Numbers

---

## 📊 Validation Reports

Generates detailed reports including

- Validation Summary
- Financial Summary
- Error Breakdown
- Failed Invoices
- Recommendations

Invalid invoices are highlighted with detailed error messages.

---

## 💾 Database Management

Powered by PostgreSQL.

Supports

- Create
- Read
- Update
- Delete
- Search
- Filtering

Users may also manually save rejected invoices using the **Save Anyway** feature.

---

## 📈 Dashboard

A modern dashboard for managing invoices.

Includes

- Statistics Cards
- Invoice Search
- Status Filters
- Invoice Details
- Edit
- Delete
- Validation Report Viewer

---

## 🔐 Authentication

JWT Authentication

- Login
- Protected Routes
- Logout

---

# 🏗 System Architecture

```text
                 Upload Invoice
                        │
                        ▼
             Detect File Type
                        │
     ┌──────────┬──────────┬──────────┐
     ▼          ▼          ▼          ▼
    CSV       Excel       PDF       Images
     │          │          │          │
     └──────────┴──────────┴──────────┘
                        │
                        ▼
              Parsing / OCR Engine
                        │
                        ▼
              Invoice Field Extraction
                        │
                        ▼
               Validation Engine
              ┌─────────┴─────────┐
              ▼                   ▼
       Valid Invoice       Invalid Invoice
              │                   │
              ▼                   ▼
      PostgreSQL Database    Validation Report
              │                   │
              └─────────┬─────────┘
                        ▼
                  React Dashboard
```

---

# 🛠 Tech Stack

| Frontend | Backend | Database | OCR |
|----------|----------|----------|----------|
| React | FastAPI | PostgreSQL | EasyOCR |
| React Router | SQLAlchemy | | Tesseract |
| Axios | Pydantic | | pdfplumber |

---

# 📸 Demo

## Login

*(Screenshot)*

---

## Upload

*(Screenshot)*

---

## Dashboard

*(Screenshot)*

---

## Validation Report

*(Screenshot)*

---

## Swagger API

*(Screenshot)*

---

# 🚀 Running the Project

## Backend

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

```
http://localhost:5173
```

---

# 🔑 Demo Login

```
Username : admin

Password : admin123
```

---

# 📡 API Endpoints

| Method | Endpoint |
|----------|----------|
| POST | `/login` |
| POST | `/upload-invoice` |
| GET | `/invoices` |
| GET | `/invoices/{id}` |
| PUT | `/invoices/{id}` |
| DELETE | `/invoices/{id}` |
| POST | `/invoices/override` |

---

# 💡 What I Learned

Building this project provided practical experience with

- Full Stack Development
- REST API Design
- OCR Pipelines
- React State Management
- PostgreSQL
- Authentication using JWT
- SQLAlchemy ORM
- File Parsing
- Data Validation
- Production-style project organization

---

# 🔮 Future Improvements

- AI-powered invoice extraction using LLMs
- Bulk processing
- Role Based Access Control
- Docker Deployment
- Cloud Deployment
- Analytics Dashboard
- Email Notifications

---

<div align="center">

## 👨‍💻 Developed by Dev

**B.Tech Computer Science Engineering**

UPES Dehradun

*"Turning documents into structured data, one invoice at a time."*

⭐ If you liked this project, consider giving it a star.

</div>