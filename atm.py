"""
atm.py
Core business logic for the ATM Management System.
"""

import database as db


class InsufficientFundsError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class ATM:
    def __init__(self):
        db.init_db()
        self.current_account = None  # (account_number, name, pin, balance)

    # ---------- Account management ----------

    def open_account(self, name, pin, initial_deposit=0):
        if len(pin) != 4 or not pin.isdigit():
            raise ValueError("PIN must be exactly 4 digits.")
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative.")
        account_number = db.create_account(name, pin, initial_deposit)
        if initial_deposit > 0:
            db.log_transaction(account_number, "OPENING_DEPOSIT", initial_deposit)
        return account_number

    def authenticate(self, account_number, pin):
        account = db.get_account(account_number)
        if account is None:
            raise AuthenticationError("Account not found.")
        if account[2] != pin:
            raise AuthenticationError("Incorrect PIN.")
        self.current_account = account
        return account

    def logout(self):
        self.current_account = None

    # ---------- Transactions ----------

    def _require_login(self):
        if self.current_account is None:
            raise AuthenticationError("No account is currently logged in.")

    def check_balance(self):
        self._require_login()
        account = db.get_account(self.current_account[0])
        return account[3]

    def deposit(self, amount):
        self._require_login()
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        account_number = self.current_account[0]
        new_balance = self.check_balance() + amount
        db.update_balance(account_number, new_balance)
        db.log_transaction(account_number, "DEPOSIT", amount)
        return new_balance

    def withdraw(self, amount):
        self._require_login()
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        current_balance = self.check_balance()
        if amount > current_balance:
            raise InsufficientFundsError("Insufficient funds for this withdrawal.")
        account_number = self.current_account[0]
        new_balance = current_balance - amount
        db.update_balance(account_number, new_balance)
        db.log_transaction(account_number, "WITHDRAWAL", amount)
        return new_balance

    def transaction_history(self):
        self._require_login()
        return db.get_transactions(self.current_account[0])

    # ---------- Admin ----------

    def list_all_accounts(self):
        return db.get_all_accounts()