"""
main.py
Command-line interface for the ATM Management System.

Run with:  python main.py
"""

from atm import ATM, AuthenticationError, InsufficientFundsError


def pause():
    input("\nPress Enter to continue...")


def open_account_flow(atm):
    print("\n--- Open New Account ---")
    name = input("Full name: ").strip()
    pin = input("Set a 4-digit PIN: ").strip()
    try:
        deposit_str = input("Initial deposit (optional, press Enter to skip): ").strip()
        initial_deposit = float(deposit_str) if deposit_str else 0
        account_number = atm.open_account(name, pin, initial_deposit)
        print(f"\nAccount created successfully! Your account number is: {account_number}")
        print("Keep this number safe — you'll need it along with your PIN to log in.")
    except ValueError as e:
        print(f"Error: {e}")
    pause()


def login_flow(atm):
    print("\n--- Login ---")
    try:
        account_number = int(input("Account number: ").strip())
        pin = input("PIN: ").strip()
        account = atm.authenticate(account_number, pin)
        print(f"\nWelcome, {account[1]}!")
        session_menu(atm)
    except (ValueError, AuthenticationError) as e:
        print(f"Login failed: {e}")
        pause()


def session_menu(atm):
    while True:
        print("\n--- Account Menu ---")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transaction History")
        print("5. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            print(f"\nCurrent balance: ${atm.check_balance():.2f}")
            pause()
        elif choice == "2":
            try:
                amount = float(input("Amount to deposit: $").strip())
                new_balance = atm.deposit(amount)
                print(f"Deposit successful. New balance: ${new_balance:.2f}")
            except ValueError as e:
                print(f"Error: {e}")
            pause()
        elif choice == "3":
            try:
                amount = float(input("Amount to withdraw: $").strip())
                new_balance = atm.withdraw(amount)
                print(f"Withdrawal successful. New balance: ${new_balance:.2f}")
            except (ValueError, InsufficientFundsError) as e:
                print(f"Error: {e}")
            pause()
        elif choice == "4":
            history = atm.transaction_history()
            if not history:
                print("\nNo transactions yet.")
            else:
                print("\n--- Transaction History ---")
                for tx_type, amount, timestamp in history:
                    print(f"{timestamp} | {tx_type:<16} | ${amount:.2f}")
            pause()
        elif choice == "5":
            atm.logout()
            print("Logged out successfully.")
            break
        else:
            print("Invalid option, please try again.")


def admin_flow(atm):
    print("\n--- All Accounts (Admin View) ---")
    accounts = atm.list_all_accounts()
    if not accounts:
        print("No accounts found.")
    else:
        print(f"{'Acct #':<10}{'Name':<20}{'Balance':>10}")
        print("-" * 40)
        for account_number, name, balance in accounts:
            print(f"{account_number:<10}{name:<20}{balance:>10.2f}")
    pause()


def main():
    atm = ATM()
    while True:
        print("\n========== ATM Management System ==========")
        print("1. Open New Account")
        print("2. Login")
        print("3. Admin: View All Accounts")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            open_account_flow(atm)
        elif choice == "2":
            login_flow(atm)
        elif choice == "3":
            admin_flow(atm)
        elif choice == "4":
            print("\nThank you for using the ATM. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()