
import logging
from pydantic import BaseModel
import os
from database import get_connection, save_transaction_and_update_balance, get_transactions, get_transactions_by_category, user_by_id, create_tables
from exceptions import InsufficientBalanceError, UserNotFoundError, ExpenseTrackerError
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from tracker import log_expense, log_income, get_balance, get_spending_by_category
from auth import register_user, login_user

class RegisterRequest(BaseModel):
    username: str
    password: str
    name: str
    age: int

class LoginRequest(BaseModel):
    username: str
    password: str

class ExpenseRequest(BaseModel):
    user_id : str
    amount: float
    category: str
    description: str = ""

class IncomeRequest(BaseModel):
    user_id : str
    amount: float
    source: str
    description: str = ""

    
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Expensive", version="1.0.0")

create_tables()  # Ensure tables are created when the app starts

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def home():
    """Health check endpoint."""
    logger.info("Health check called")
    return {"message": "Expensive API is live 🚀"}

@app.post("/register", tags=["Authentication"])
def register(request: RegisterRequest):
    """Register a new user."""
    try:
        register_user(request.username, request.password, request.name, request.age)
        logger.info(f"User '{request.username}' registered successfully.")
        return {"status": "success", "message": "User registered successfully."}
    except ExpenseTrackerError as e:
        logger.error(f"Registration failed for user '{request.username}': {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/login", tags=["Authentication"])
def login(request: LoginRequest):
    """Login a user."""
    try:
        user = login_user(request.username, request.password)
        safe_password = {k: v for k, v in user.items() if k != "password"}
        logger.info(f"User '{request.username}' logged in successfully.")
        return {"status": "success", "message": "Login successful.", "user": safe_password}
    except ExpenseTrackerError as e:
        logger.error(f"Login failed for user '{request.username}': {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/balance/{user_id}")
def get_user_balance(user_id: str):
    """fetch balance of user"""
    try:
        balance = get_balance(user_id)
        logger.info(f"Balance Shown {user_id}")
        return {"status": "success", "balance": balance}
    except UserNotFoundError as e:
        logger.error(f"User not Present : {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    
@app.get("/spending/{user_id}/{category}")
def get_user_spending(user_id: str, category: str):
    """fetch spending of user"""
    try:
        expenditure = get_spending_by_category(user_id, category)
        logger.info(f"Expenditure of User {user_id} on {category}")
        return {"status": "success", "category": category, "total_spent": expenditure}
    except UserNotFoundError as e:
        logger.error(f"User not Present: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    
@app.post("/expense", tags=["Expenses"])
def create_expense(request: ExpenseRequest):
    "add new expense"
    try:
        spending = log_expense(request.user_id, request.amount, request.category, request.description)
        logger.info(f"Added A expenditure from {request.user_id} in category {request.category} of amount {request.amount}")
        return spending
    except UserNotFoundError as e:
        logger.error(f"User not Present: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except InsufficientBalanceError as e:
        logger.error(f"User:{request.user_id} has Insufficient balance for expense of {request.amount} ")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/income", tags=["Income"])
def create_income(request: IncomeRequest):
    "add new income"
    try:
        income = log_income(request.user_id, request.amount, request.source, request.description)
        logger.info(f"Added a Income from {request.user_id} from source {request.source} of amount {request.amount}")
        return income
    except UserNotFoundError as e:
        logger.error(f"User not Present: {str(e)}")
