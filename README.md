# Banking_System
This project is a Banking Management System built using Python (for the backend logic) and MySQL (for database storage). It simulates core banking operations such as account creation, deposits, withdrawals, fund transfers, balance checks, and transaction history tracking.

**Overview**
This project implements a secure banking system that allows customers to perform basic banking operations while administrators can manage accounts. The system uses Python for the application logic and MySQL for data storage.

**Features**
Customer Features
Account creation with secure password hashing

**Balance inquiry**

Cash deposits and withdrawals

Fund transfers between accounts

Transaction history viewing

Personal details management

**Admin Features**
View all customer accounts

Create/delete accounts

Freeze/unfreeze accounts

View transaction logs

Generate system reports

**Technologies Used**
Python 3.x (Core application)

MySQL (Database)

mysql-connector-python (Database connectivity)

hashlib (Password security)

datetime (Transaction timestamps)

Prerequisites
Python 3.6+

MySQL Server 5.7+

mysql-connector-python package

Basic understanding of relational databases

**Installation**
Clone the repository:

bash
git clone https://github.com/yourusername/banking-system.git
cd banking-system
Set up the database:

Install MySQL if not already installed

Create a new database named bank_system

Run the SQL script from database/setup.sql to create tables

**Install dependencies:**

bash
pip install mysql-connector-python
Configure database connection:
Edit config.py with your MySQL credentials:

python
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'bank_system'
}
Usage
**Run the application:**

bash
python main.py
Login options:

Customer: Use account number and password

Admin: Use admin credentials (setup during installation)

Follow the menu prompts to perform banking operations.

**Database Schema**
The system uses the following main tables:

customers - Stores customer personal information

accounts - Contains account details and balances

transactions - Records all financial transactions

admins - Stores administrator credentials
**
Security Features**
Password hashing with SHA-256

Session timeouts for inactive users

Input validation to prevent SQL injection

Transaction logging for audit purposes

Future Enhancements
Mobile app integration

**Online banking portal**

**Check deposit functionality**

Loan application module

Biometric authentication

Contributing
Contributions are welcome! Please fork the repository and submit pull requests.
