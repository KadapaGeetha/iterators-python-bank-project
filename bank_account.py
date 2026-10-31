

from decimal import Decimal

class BankAccount:

    def __init__(self, account_number, customer_name, balance):
        self.account_number = account_number
        self.customer_name = customer_name
        self.balance = balance

    def display_details(self):
        print("Account Number:", self.account_number)
        print("Customer Name:", self.customer_name)
        print("Current Balance:", self.balance)

    def create_account(self, con):
        cursor = con.cursor()

        try:
            query = """
            INSERT INTO accounts
            (account_number, customer_name, balance)
            VALUES (%s, %s, %s)
            """

            values = (
                self.account_number,
                self.customer_name,
                self.balance
            )

            cursor.execute(query, values)

            cursor.execute("""
                INSERT INTO transactions
                (account_number, transaction_type, amount, balance)
                VALUES (%s, %s, %s, %s)
            """, (
                self.account_number,
                "Initial Deposit",
                self.balance,
                self.balance
            ))

            con.commit()
            print("Account Created Successfully!")

        except Exception as e:
            con.rollback()
            print("Error:", e)

        finally:
            cursor.close()

    def check_balance(self, con):
        cursor = con.cursor()

        try:
            query = """
            SELECT customer_name, balance
            FROM accounts
            WHERE account_number = %s
            """

            cursor.execute(query, (self.account_number,))
            result = cursor.fetchone()

            if result:
                print("\nCustomer Name:", result[0])
                print("Available Balance:", result[1])
            else:
                print("\nAccount Not Found!")

        except Exception as e:
            print("Error:", e)

        finally:
            cursor.close()

    def deposit(self, con, amount):
        cursor = con.cursor()

        try:
            if amount <= 0:
                print("Enter a valid deposit amount!")
                return

            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = %s",
                (self.account_number,)
            )

            result = cursor.fetchone()

            if result is None:
                print("Account Not Found!")
                return

            current_balance = Decimal(str(result[0]))
            amount = Decimal(str(amount))
            new_balance = current_balance + amount

            cursor.execute("""
                UPDATE accounts
                SET balance = %s
                WHERE account_number = %s
            """, (new_balance, self.account_number))

            cursor.execute("""
                INSERT INTO transactions
                (account_number, transaction_type, amount, balance)
                VALUES (%s, %s, %s, %s)
            """, (
                self.account_number,
                "Deposit",
                amount,
                new_balance
            ))

            con.commit()

            self.balance = new_balance

            print("\nDeposit Successful!")
            print("Deposited Amount:", amount)
            print("Available Balance:", new_balance)

        except Exception as e:
            con.rollback()
            print("Error:", e)

        finally:
            cursor.close()



    def withdraw(self, con, amount):
        cursor = con.cursor()

        try:
            if amount <= 0:
                print("Enter a valid withdrawal amount!")
                return

            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number = %s",
                (self.account_number,)
            )

            result = cursor.fetchone()

            if result is None:
                print("Account Not Found!")
                return

            current_balance = Decimal(str(result[0]))
            amount = Decimal(str(amount))

            if amount > current_balance:
                print("Insufficient Balance!")
                return

            new_balance = current_balance - amount

            cursor.execute("""
                UPDATE accounts
                SET balance = %s
                WHERE account_number = %s
            """, (new_balance, self.account_number))

            cursor.execute("""
                INSERT INTO transactions
                (account_number, transaction_type, amount, balance)
                VALUES (%s, %s, %s, %s)
            """, (
                self.account_number,
                "Withdrawal",
                amount,
                new_balance
            ))

            con.commit()

            self.balance = new_balance

            print("\nWithdrawal Successful!")
            print("Withdrawn Amount:", amount)
            print("Available Balance:", new_balance)

        except Exception as e:
            con.rollback()
            print("Error:", e)

        finally:
            cursor.close()

    def transaction_history(self, con):
        cursor = con.cursor()

        try:
            query = """
            SELECT transaction_type, amount, balance
            FROM transactions
            WHERE account_number = %s
            ORDER BY transaction_id DESC
            """

            cursor.execute(query, (self.account_number,))
            records = cursor.fetchall()

            if records:
                print("\n----- TRANSACTION HISTORY -----")

                for row in records:
                    print("----------------------------")
                    print("Transaction Type:", row[0])
                    print("Amount:", row[1])
                    print("Balance:", row[2])
            else:
                print("No Transactions Found!")

        except Exception as e:
            print("Error:", e)

        finally:
            cursor.close()

