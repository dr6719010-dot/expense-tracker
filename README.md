# expense-tracker
#personal note
Hello, Back again this one didn't took that much time and i could really focus on workflow and data flow in this project and things went much smoother. i am going to add more features as i am also learning while building so it takes time. show goos response, point out bugs, and any type of suggestions u have.

# Expensive 💰

A simple Expense Tracker API built with FastAPI and SQLite.

Track income, expenses, account balance, and spending by category through a REST API with user authentication.

## 🚀 Live Demo

https://expensive-jnbb.onrender.com

## ✨ Features

- User Registration
- User Login Authentication
- Password Hashing (SHA-256)
- Track Income
- Track Expenses
- Real-Time Balance Updates
- Spending Analysis by Category
- SQLite Database Storage
- Custom Exception Handling
- FastAPI Documentation Support
- Deployed on Render

---

## 🛠️ Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- SQLite

### Deployment
- Render

### Version Control
- Git
- GitHub

---

## 📂 Project Structure

```text
expense-tracker/
│
├── main.py           # FastAPI routes
├── auth.py           # Authentication logic
├── tracker.py        # Income and expense tracking
├── database.py       # SQLite operations
├── models.py         # Pydantic models
├── exceptions.py     # Custom exceptions
├── requirements.txt
└── README.md
```

---

## 🔑 API Endpoints

### Authentication

| Method | Endpoint | Description |
|----------|------------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login existing user |

### Financial Operations

| Method | Endpoint | Description |
|----------|------------|-------------|
| POST | `/income` | Add income |
| POST | `/expense` | Add expense |
| GET | `/balance/{user_id}` | Get current balance |
| GET | `/spending/{user_id}/{category}` | Get spending by category |

---

## Example Register Request

```json
POST /register

{
  "username": "john123",
  "password": "mypassword",
  "name": "John Doe",
  "age": 20
}
```

---

## Example Login Request

```json
POST /login

{
  "username": "john123",
  "password": "mypassword"
}
```

---

## Running Locally

Clone the repository:

```bash
git clone https://github.com/dr6719010-dot/expense-tracker.git
```

Move into project directory:

```bash
cd expense-tracker
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start server:

```bash
uvicorn main:app --reload
```

Server will run on:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Learning Outcomes

This project helped me learn:

- REST API Design
- FastAPI Development
- SQLite Database Integration
- Authentication Systems
- Password Hashing
- Error Handling
- Git & GitHub Workflow
- Deployment on Render
- Production Debugging

---

## Future Improvements

- JWT Authentication
- PostgreSQL Integration
- Transaction History Endpoint
- User Budget Management
- Docker Support
- Frontend Dashboard Improvements

---

## Author

Digvijay Rana

Second backend project built after completing a Calculator API. Created to deepen understanding of authentication, database design, API architecture, and deployment workflows.
