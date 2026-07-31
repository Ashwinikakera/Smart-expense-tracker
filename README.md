# Smart Expense Tracker API

A REST API built with **Python** and **FastAPI** to manage personal expenses. The application stores expense data in a local JSON file, eliminating the need for a database while providing persistent storage.

## Features

- Add a new expense
- View all expenses
- Filter expenses by category
- Calculate:
  - Overall expenses
  - Category-wise expense totals
- Delete an expense by ID
- Input validation using Pydantic
- Automatic API documentation with Swagger UI

---

## Tech Stack

- Python 3.10+
- FastAPI
- Pydantic
- Uvicorn
- Pytest

---

## Project Structure

```
your-repo/
│── README.md
│── AI_NOTES.md
│── requirements.txt
│
├── src/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   └── services/
│
├── tests/
│   ├── conftest.py
│   └── test_expenses.py
│
└── data/
    └── expenses.json
```

---

# Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd your-repo
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```


# Run the Server

Start the FastAPI development server:

```bash
uvicorn src.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger API documentation:

```
http://127.0.0.1:8000/docs
```



# Run the Tests

Execute all unit tests using:

```bash
python -m pytest -v
```

The test suite uses temporary test data and does not modify the production JSON file.

# Available API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/expenses` | Add a new expense |
| GET | `/expenses` | Retrieve all expenses |
| GET | `/expenses?category={category}` | Filter expenses by category |
| GET | `/expenses/totals` | Get overall and category-wise expense totals |
| DELETE | `/expenses/{expense_id}` | Delete an expense |
| GET | `/health` | Health check endpoint |

# Data Storage

Expenses are stored in:
data/expenses.json

The file is automatically created when the first expense is added.


# Validation

The API validates incoming requests using Pydantic:

- Title is required.
- Category is required.
- Amount must be greater than zero.
- Date must be in ISO format (`YYYY-MM-DD`).

Invalid requests return appropriate HTTP status codes.




