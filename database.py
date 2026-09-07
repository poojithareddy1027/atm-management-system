"""
database.py
Handles all SQLite database operations for the ATM Management System.
"""

import sqlite3
import os

DB_NAME = "atm.db"


def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Create the accounts and transactions tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            account_number INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            pin TEXT NOT NULL,
            balance REAL NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_number INTEGER NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_number) REFERENCES accounts(account_number)
        )
    """)

    conn.commit()
    conn.close()


def create_account(name, pin, initial_deposit=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO accounts (name, pin, balance) VALUES (?, ?, ?)",
        (name, pin, initial_deposit),
    )
    account_number = cursor.lastrowid
    conn.commit()
    conn.close()
    return account_number


def get_account(account_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT account_number, name, pin, balance FROM accounts WHERE account_number = ?",
        (account_number,),
    )
    row = cursor.fetchone()
    conn.close()
    return row


def update_balance(account_number, new_balance):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE accounts SET balance = ? WHERE account_number = ?",
        (new_balance, account_number),
    )
    conn.commit()
    conn.close()


def log_transaction(account_number, tx_type, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (account_number, type, amount) VALUES (?, ?, ?)",
        (account_number, tx_type, amount),
    )
    conn.commit()
    conn.close()


def get_transactions(account_number):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT type, amount, timestamp FROM transactions WHERE account_number = ? ORDER BY id DESC",
        (account_number,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_accounts():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT account_number, name, balance FROM accounts")
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_db():
    """Utility for resetting the database during testing."""
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)