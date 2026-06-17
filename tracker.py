"""

This module contains the Tracker class, which is responsible for tracking the expenditures of users in the Expense Tracker application. The Tracker class provides methods for adding transactions, calculating total expenses, and generating reports.

The Tracker class interacts with the database to store and retrieve transaction data, and it also handles various exceptions that may arise during the tracking process. It ensures that users can effectively manage their expenses and stay within their budgets.
"""
from database import save_transaction_and_update_balance, get_transactions, get_transactions_by_category, user_by_id
from exceptions import InsufficientBalanceError, UserNotFoundError
from models import Transaction
def calculate_new_balance(user_id, amount, transaction_type):
    user = user_by_id(user_id)
    if not user:
        raise UserNotFoundError(f"User with id '{user_id}' not found.")
    
    if transaction_type == "expense":
        if user['balance'] < amount:
            raise InsufficientBalanceError("Insufficient balance for this transaction.")
        return user['balance'] - amount
    elif transaction_type == "income":
        return user['balance'] + amount
    else:
        raise ValueError("Invalid transaction type. Must be 'income' or 'expense'.")
    

def log_expense(user_id, amount, category, description=""):
    """Log an expense or income for a user."""
    new_balance = calculate_new_balance(user_id, amount, transaction_type="expense")
    
    
    transaction = Transaction(
        user_id=user_id,
        amount=amount,
        category=category,
        type="expense",
        description=description
    )
    
    save_transaction_and_update_balance(transaction, new_balance)
    
    is_zero = (new_balance == 0)
    status = "warning" if is_zero else "success"
    message = "Your account balance has hit 0." if is_zero else "Expense logged successfully."
    
    
    return {
        "status": status,
        "message": message,
        "new_balance": new_balance,
        "transaction": transaction.model_dump()
    }


def log_income(user_id, amount, category, description=""):
    """Log an income for a user."""
    new_balance = calculate_new_balance(user_id, amount, transaction_type="income")
    
    
    transaction = Transaction(
        user_id=user_id,
        amount=amount,
        category=category,
        type="income",
        description=description
    )
    
    save_transaction_and_update_balance(transaction, new_balance)
    
    return {
        "status": "success",
        "message": "Income logged successfully.",
        "new_balance": new_balance,
        "transaction": transaction.model_dump()
    }

def get_balance(user_id):
    """Get the current balance of a user."""
    user = user_by_id(user_id)
    if not user:
        raise UserNotFoundError(f"User with id '{user_id}' not found.")
    return user['balance']

def get_spending_by_category(user_id, category):
    """Get the total spending of a user by category."""
    # 1. Explicitly verify the user exists first
    if not user_by_id(user_id):
        raise UserNotFoundError(f"User with id '{user_id}' not found.")
        
    transactions = get_transactions_by_category(user_id, category)
    if not transactions:
        return 0.0  # Safe to return 0 now, because we know the user is real
        
    return sum(t['amount'] for t in transactions if t['type'] == "expense")
