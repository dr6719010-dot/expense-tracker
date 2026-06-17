import sqlite3
from datetime import datetime

DB_NAME = "expense_tracker.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id    TEXT PRIMARY KEY,
    username   TEXT UNIQUE NOT NULL,
    password   TEXT NOT NULL,
    name       TEXT NOT NULL,
    balance    REAL DEFAULT 0.0,
    budget     REAL DEFAULT 0.0,
    age        INTEGER,
    created_at TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
        id          TEXT PRIMARY KEY,
    user_id     TEXT NOT NULL,
    amount      REAL NOT NULL,
    category    TEXT NOT NULL,
    type        TEXT NOT NULL,
    description TEXT DEFAULT '',
    created_at  TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
                   )
            """)
                   
    
    conn.commit()
    conn.close()


def save_user(user):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, username, password, name, balance, budget, age, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user.user_id, user.username, user.password, user.name, user.balance, user.budget, user.age, user.created_at))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "user_id": row[0],
            "username": row[1],
            "password": row[2],
            "name": row[3],
            "balance": row[4],
            "budget": row[5],
            "age": row[6],
            "created_at": row[7]
        }
    return None

def user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "user_id": row[0],
            "username": row[1],
            "password": row[2],
            "name": row[3],
            "balance": row[4],
            "budget": row[5],
            "age": row[6],
            "created_at": row[7]
        }
    return None

def update_user_balance(user_id, new_balance):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()

def save_transaction(transaction):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (id, user_id, amount, category, type, description, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (transaction.id, transaction.user_id, transaction.amount, transaction.category, transaction.type, transaction.description, transaction.created_at))
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    transactions = []
    for row in rows:
        transactions.append({
            "id": row[0],
            "user_id": row[1],
            "amount": row[2],
            "category": row[3],
            "type": row[4],
            "description": row[5],
            "created_at": row[6]
        })
    return transactions

def get_transactions_by_category(user_id, category):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE user_id = ? AND category = ?", (user_id, category))
    rows = cursor.fetchall()
    conn.close()
    transactions = []
    for row in rows:
        transactions.append({
            "id": row[0],
            "user_id": row[1],
            "amount": row[2],
            "category": row[3],
            "type": row[4],
            "description": row[5],
            "created_at": row[6]
        })
    return transactions

def save_transaction_and_update_balance(transaction, new_balance):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        conn.execute('BEGIN')

        cursor.execute("""
            INSERT INTO transactions (id, user_id, amount, category, type, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (transaction.id, transaction.user_id, transaction.amount,
              transaction.category, transaction.type, transaction.description, transaction.created_at))

        cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?",
                        (new_balance, transaction.user_id))

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()