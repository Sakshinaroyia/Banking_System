import mysql.connector
from mysql.connector import Error

# Database Connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='banking_system',
            user='Sakshi',    # Change to your MySQL username
            password='Mukti@4521'     # Change to your MySQL password
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# 1. Create a New Account
def create_account():
    print("\n--- Create New Account ---")
    name = input("Customer Name: ")
    email = input("Email: ")
    phone = input("Phone Number: ")
    initial_deposit = float(input("Initial Deposit Amount: ₹"))

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Insert customer
            query = "INSERT INTO customers (name, balance, email, phone) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, initial_deposit, email, phone))
            account_number = cursor.lastrowid

            # Record transaction
            query = """INSERT INTO transactions 
                      (account_number, amount, transaction_type) 
                      VALUES (%s, %s, 'DEPOSIT')"""
            cursor.execute(query, (account_number, initial_deposit))
            
            conn.commit()
            print(f"\nAccount created successfully! Account Number: {account_number}")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# 2. Deposit Money
def deposit_money():
    print("\n--- Deposit Money ---")
    account_number = int(input("Account Number: "))
    amount = float(input("Amount to Deposit: ₹"))

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Update balance
            query = "UPDATE customers SET balance = balance + %s WHERE account_number = %s"
            cursor.execute(query, (amount, account_number))

            # Record transaction
            query = """INSERT INTO transactions 
                      (account_number, amount, transaction_type) 
                      VALUES (%s, %s, 'DEPOSIT')"""
            cursor.execute(query, (account_number, amount))
            
            conn.commit()
            print(f"\n₹{amount} deposited successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# 3. Withdraw Money
def withdraw_money():
    print("\n--- Withdraw Money ---")
    account_number = int(input("Account Number: "))
    amount = float(input("Amount to Withdraw: ₹"))

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Check balance
            cursor.execute("SELECT balance FROM customers WHERE account_number = %s", (account_number,))
            balance = cursor.fetchone()[0]

            if balance < amount:
                print("\nInsufficient balance!")
                return

            # Update balance
            query = "UPDATE customers SET balance = balance - %s WHERE account_number = %s"
            cursor.execute(query, (amount, account_number))

            # Record transaction
            query = """INSERT INTO transactions 
                      (account_number, amount, transaction_type) 
                      VALUES (%s, %s, 'WITHDRAWAL')"""
            cursor.execute(query, (account_number, amount))
            
            conn.commit()
            print(f"\n₹{amount} withdrawn successfully!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# 4. Transfer Money
def transfer_money():
    print("\n--- Transfer Money ---")
    from_account = int(input("Your Account Number: "))
    to_account = int(input("Receiver's Account Number: "))
    amount = float(input("Amount to Transfer: ₹"))

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Check sender's balance
            cursor.execute("SELECT balance FROM customers WHERE account_number = %s", (from_account,))
            sender_balance = cursor.fetchone()[0]

            if sender_balance < amount:
                print("\nInsufficient balance!")
                return

            # Check if receiver exists
            cursor.execute("SELECT 1 FROM customers WHERE account_number = %s", (to_account,))
            if not cursor.fetchone():
                print("\nReceiver account not found!")
                return

            # Deduct from sender
            query = "UPDATE customers SET balance = balance - %s WHERE account_number = %s"
            cursor.execute(query, (amount, from_account))

            # Add to receiver
            query = "UPDATE customers SET balance = balance + %s WHERE account_number = %s"
            cursor.execute(query, (amount, to_account))

            # Record transactions
            query = """INSERT INTO transactions 
                      (account_number, amount, transaction_type, related_account) 
                      VALUES (%s, %s, 'TRANSFER', %s)"""
            cursor.execute(query, (from_account, amount, to_account))
            cursor.execute(query, (to_account, amount, from_account))
            
            conn.commit()
            print(f"\n₹{amount} transferred successfully!")
        except Error as e:
            print(f"Error: {e}")
            conn.rollback()
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# 5. Check Balance
def check_balance():
    print("\n--- Check Balance ---")
    account_number = int(input("Account Number: "))

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name, balance FROM customers WHERE account_number = %s", (account_number,))
            result = cursor.fetchone()

            if result:
                name, balance = result
                print(f"\nCustomer: {name}")
                print(f"Account Number: {account_number}")
                print(f"Available Balance: ₹{balance}")
            else:
                print("\nAccount not found!")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# 6. View Transactions
def view_transactions():
    print("\n--- Transaction History ---")
    account_number = int(input("Account Number: "))

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT name FROM customers WHERE account_number = %s", (account_number,))
            customer = cursor.fetchone()

            if not customer:
                print("\nAccount not found!")
                return

            print(f"\nCustomer: {customer['name']}")
            print(f"Account Number: {account_number}")
            print("\nTransaction History:")
            print("-" * 70)
            print(f"{'Date':<20} {'Type':<12} {'Amount':<12} {'Related Account':<20}")
            print("-" * 70)

            query = """SELECT transaction_date, transaction_type, amount, related_account 
                       FROM transactions 
                       WHERE account_number = %s 
                       ORDER BY transaction_date DESC"""
            cursor.execute(query, (account_number,))
            transactions = cursor.fetchall()

            if not transactions:
                print("No transactions found.")
            else:
                for trans in transactions:
                    date = trans['transaction_date'].strftime("%d-%m-%Y %H:%M:%S")
                    trans_type = trans['transaction_type']
                    amount = trans['amount']
                    related_acc = trans['related_account'] if trans['related_account'] else "-"
                    print(f"{date:<20} {trans_type:<12} ₹{amount:<10} {related_acc:<20}")

            print("-" * 70)
        except Error as e:
            print(f"Error: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

# Main Menu
def main_menu():
    while True:
        print("\n=== Banking Management System ===")
        print("1. Create New Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Check Balance")
        print("6. View Transactions")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            transfer_money()
        elif choice == '5':
            check_balance()
        elif choice == '6':
            view_transactions()
        elif choice == '7':
            print("\nExiting... Thank you!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()