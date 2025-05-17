# Library_Management_System--LMS--MASAI
DESCRIPTION:
------------
This is a simple command-line Library Management System written in Python.
It uses CSV files to store data about books, members, loans, and librarians.
Passwords are securely stored using bcrypt hashing.

FEATURES:
---------
Librarian:
- Login securely
- Add and remove books
- Issue and return books
- View overdue books
- Reset member passwords

Member:
- Login securely
- Request password reset
- View available books
- Borrow and return books
- View personal loan history

FILES USED:
-----------
- books.csv        => Stores book information
- members.csv      => Stores member information and hashed passwords
- loans.csv        => Stores loan records
- librarians.csv   => Stores librarian login info

REQUIREMENTS:
-------------
- Python 3.7 or higher
- bcrypt library (Install with: pip install bcrypt)

HOW TO RUN:
-----------
1. Make sure Python is installed.
2. Ensure the CSV files are present in the same directory.
3. Run the program using:

   python main.py

CSV FILE FORMATS:
-----------------
books.csv:
ISBN,Title,Author,CopiesTotal,CopiesAvailable
9780132350884,Clean Code,Robert C. Martin,5,3

members.csv:
MemberID,Name,PasswordHash,Email
1001,Ananya Singh,$2b$12$...hashed...,ananya@mail.com

loans.csv:
LoanID,MemberID,ISBN,IssueDate,DueDate,ReturnDate
1,1001,9780132350884,2025-05-10,2025-05-24,

librarians.csv:
Username,Password
admin,$2b$12$...hashed...

CREATING HASHED PASSWORDS:
--------------------------
To create a hashed password for librarians or members, use the following Python code:

    import bcrypt
    password = bcrypt.hashpw("yourpassword".encode(), bcrypt.gensalt())
    print(password.decode())

NOTES:
------
- All date formats are YYYY-MM-DD.
- Overdue loans are calculated based on today's date.
- System runs entirely in the console.

CONTACT:
--------
This project is for educational purposes.
For support, contact the project creator.
