# Inventory Management System

A full-stack inventory management system built with FastAPI, SQLAlchemy, and JavaScript.

This project demonstrates a CRUD-based inventory application that tracks bioconjugated antibody products, manufactured lots, bulk inventory, and packaged inventory through a REST API.

## Features

- Product management
- Lot tracking
- Bulk inventory management
- Packaged inventory management
- Create, edit, and delete records
- REST API with FastAPI
- Relational database using SQLAlchemy

## Technology Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic

### Database
- SQLite 

## Running Locally
### Clone the repository

```bash
git clone https://github.com/gu-olivia/DEMO-Inventory-Management-System.git
cd DEMO-Inventory-Management-System
```

### Install dependencies

```bash
pip install -r backend/requirements.txt
```

### Start the backend

```bash
uvicorn main:app --reload
```

### Open the frontend

Open `frontend/index.html` in your browser.

## Future Improvements

- Search and filtering
- Pagination
- Inventory analytics dashboard
- Inventory change loggging
- QR code generation 
- Export to Excel
- Automated inventory alerts
- Integration with customer order history
  

## License

This project is intended for educational and portfolio purposes.
