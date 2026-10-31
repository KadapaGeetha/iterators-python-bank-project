
# 
# from database import create_connection
# from bank_account import BankAccount

# con = create_connection()

# if con:

#     account_number = int(input("Enter Account Number: "))

#     account = BankAccount(account_number, "", 0)

#     account.check_balance(con)

#     con.close()


# from database import create_connection
# from bank_account import BankAccount

# con = create_connection()

# if con:
#     account_number = int(input("Enter Account Number: "))
#     amount = float(input("Enter Deposit Amount: "))

#     account = BankAccount(account_number, "", 0)

#     account.deposit(con, amount)

#     con.close()


# from database import create_connection
# from bank_account import BankAccount

# con = create_connection()

# if con:
#     account_number = int(input("Enter Account Number: "))
#     amount = float(input("Enter Withdrawal Amount: "))

#     account = BankAccount(account_number, "", 0)

#     account.withdraw(con, amount)

#     con.close()


# from database import create_connection
# from bank_account import BankAccount

# con = create_connection()

# if con:
#     account_number = int(input("Enter Account Number: "))

#     account = BankAccount(account_number, "", 0)

#     account.transaction_history(con)

#     con.close()


from decimal import Decimal, InvalidOperation

from database import create_connection
from bank_account import BankAccount


# Account number validation
def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))

            if value <= 0:
                print("Please enter a positive number!")
            else:
                return value

        except ValueError:
            print("Invalid input! Please enter numbers only.")


# Amount validation
def get_positive_amount(prompt):
    while True:
        try:
            amount = Decimal(input(prompt))

            if not amount.is_finite() or amount <= 0:
                print("Please enter a valid positive amount!")
            else:
                return amount

        except InvalidOperation:
            print("Invalid amount! Please enter numbers only.")


# Database connection
con = create_connection()

if con:

    while True:

        print("\n===== BANK MANAGEMENT SYSTEM =====")
        print("1. Create Account")
        print("2. Check Balance")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transaction History")
        print("6. Exit")

        choice = input("\nEnter Your Choice: ")

        if choice == "1":

            account_number = get_positive_int("Enter Account Number: ")
            customer_name = input("Enter Customer Name: ").strip()
            
            if not customer_name:
                print("Customer name cannot be empty!")
                continue

            balance = get_positive_amount("Enter Initial Deposit: ")

            account = BankAccount(
                account_number,
                customer_name,
                balance
            )

            account.create_account(con)

        elif choice == "2":

            account_number = get_positive_int("Enter Account Number: ")

            account = BankAccount(account_number, "", 0)
            account.check_balance(con)

        elif choice == "3":

            account_number = get_positive_int("Enter Account Number: ")
            amount = get_positive_amount("Enter Deposit Amount: ")

            account = BankAccount(account_number, "", 0)
            account.deposit(con, amount)

        elif choice == "4":

            account_number = get_positive_int("Enter Account Number: ")
            amount = get_positive_amount("Enter Withdrawal Amount: ")

            account = BankAccount(account_number, "", 0)
            account.withdraw(con, amount)

        elif choice == "5":

            account_number = get_positive_int("Enter Account Number: ")

            account = BankAccount(account_number, "", 0)
            account.transaction_history(con)

        elif choice == "6":

            print("\nThank you for using Bank Management System!")
            break

        else:
            print("Invalid Choice! Please try again.")

    con.close()
