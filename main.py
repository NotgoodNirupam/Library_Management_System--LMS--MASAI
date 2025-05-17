import csv
import bcrypt
import os
from datetime import datetime, timedelta

# === Helper Functions ===
def load_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, newline='') as f:
        return list(csv.DictReader(f))

def save_csv(filename, data, fieldnames):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def append_csv(filename, row, fieldnames):
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(row)

# === Member Login ===
def login_member():
    members = load_csv('members.csv')
    member_id = input("Enter Member ID: ")
    password = input("Enter Password: ")
    for member in members:
        if member['MemberID'] == member_id:
            if bcrypt.checkpw(password.encode(), member['PasswordHash'].encode()):
                print(f"Welcome back, {member['Name']}!")
                return member
            else:
                print("Incorrect password.")
                return None
    print("Member ID not found.")
    return None

# === Password Reset ===
def request_password_reset():
    member_id = input("Enter your Member ID for password reset: ")
    
    # Check if the member ID is empty
    if not member_id.strip():
        print("Member ID cannot be empty. Returning to the menu.")
        input("\nPress Enter to return to the main menu...")
        return
    
    members = load_csv('members.csv')
    found = False
    for member in members:
        if member['MemberID'] == member_id:
            found = True
            print("Password reset requested. Please wait for librarian assistance.")
            break
    
    if not found:
        print("Member ID not found. Returning to menu.")
    
    input("\nPress Enter to return to the main menu...")

# === Librarian Login ===
def login_librarian():
    librarians = load_csv('librarians.csv')
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    for librarian in librarians:
        if librarian['Username'] == username:
            if bcrypt.checkpw(password.encode(), librarian['Password'].encode()):
                print(f"Welcome, Librarian {librarian['Username']}!")
                return True
            else:
                print("Incorrect password.")
                return False
    print("Librarian username not found.")
    return False

# === Main Menu ===
def main_menu():
    while True:
        print("\n=== Library Management System ===")
        print("1. Member Login")
        print("2. Request Password Reset")
        print("3. Librarian Login")
        print("4. Exit")
        choice = input("> ")

        if choice == '1':
            member = login_member()
            if member:
                member_menu(member)
        elif choice == '2':
            request_password_reset()
        elif choice == '3':
            if login_librarian():
                librarian_menu()
        elif choice == '4':
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Try again.")

# === Member Menu ===
def member_menu(member):
    while True:
        print("\n=== Member Menu ===")
        print("1. View Available Books")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View My Loans")
        print("5. Logout")
        choice = input("> ")

        if choice == '1':
            list_books()
        elif choice == '2':
            issue_book(member)
        elif choice == '3':
            return_book(member)
        elif choice == '4':
            view_loans(member)
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

# === Librarian Menu ===
def librarian_menu():
    while True:
        print("\n=== Librarian Dashboard ===")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. View Overdue Books")
        print("4. Reset Member Password")
        print("5. Logout")
        choice = input("> ")

        if choice == '1':
            add_book()
        elif choice == '2':
            remove_book()
        elif choice == '3':
            view_overdue()
        elif choice == '4':
            reset_member_password()
        elif choice == '5':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

# === Book Functions ===
def list_books():
    books = load_csv('books.csv')
    print("\nAvailable Books:")
    for book in books:
        print(f"{book['ISBN']} | {book['Title']} by {book['Author']} | Available: {book['CopiesAvailable']}")
    print()

def issue_book(member):
    isbn = input("Enter ISBN to issue: ")
    books = load_csv('books.csv')
    book = next((b for b in books if b['ISBN'] == isbn), None)
    if not book or int(book['CopiesAvailable']) < 1:
        print("Book not available.")
        return
    book['CopiesAvailable'] = str(int(book['CopiesAvailable']) - 1)
    save_csv('books.csv', books, books[0].keys())

    loans = load_csv('loans.csv')
    new_loan = {
        'LoanID': str(len(loans) + 1),
        'MemberID': member['MemberID'],
        'ISBN': isbn,
        'IssueDate': datetime.today().strftime('%Y-%m-%d'),
        'DueDate': (datetime.today() + timedelta(days=14)).strftime('%Y-%m-%d'),
        'ReturnDate': ''
    }
    append_csv('loans.csv', new_loan, new_loan.keys())
    print(f"Book issued. Due on {new_loan['DueDate']}.")

def return_book(member):
    isbn = input("Enter ISBN to return: ")
    loans = load_csv('loans.csv')
    for loan in loans:
        if loan['MemberID'] == member['MemberID'] and loan['ISBN'] == isbn and loan['ReturnDate'] == '':
            loan['ReturnDate'] = datetime.today().strftime('%Y-%m-%d')
            break
    else:
        print("No active loan found for this book.")
        return
    save_csv('loans.csv', loans, loans[0].keys())

    books = load_csv('books.csv')
    book = next((b for b in books if b['ISBN'] == isbn), None)
    if book:
        book['CopiesAvailable'] = str(int(book['CopiesAvailable']) + 1)
        save_csv('books.csv', books, books[0].keys())
    print("Book returned successfully.")

def view_loans(member):
    loans = load_csv('loans.csv')
    print("\nYour Loans:")
    for loan in loans:
        if loan['MemberID'] == member['MemberID']:
            print(f"Book ISBN: {loan['ISBN']} | Issued: {loan['IssueDate']} | Due: {loan['DueDate']} | Returned: {loan['ReturnDate'] or 'Not yet returned'}")
    print()

# === Librarian Functions ===
def add_book():
    isbn = input("Enter ISBN: ")
    books = load_csv('books.csv')
    if next((b for b in books if b['ISBN'] == isbn), None):
        print("Book already exists!")
        return
    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    copies = input("Enter Number of Copies: ")
    book = {
        'ISBN': isbn,
        'Title': title,
        'Author': author,
        'CopiesTotal': copies,
        'CopiesAvailable': copies
    }
    append_csv('books.csv', book, book.keys())
    print("Book added successfully.")

def remove_book():
    isbn = input("Enter ISBN to remove: ")
    books = load_csv('books.csv')
    updated_books = [book for book in books if book['ISBN'] != isbn]
    if len(books) == len(updated_books):
        print("Book not found!")
        return
    save_csv('books.csv', updated_books, books[0].keys())
    print("Book removed successfully.")

def view_overdue():
    loans = load_csv('loans.csv')
    today = datetime.today().strftime('%Y-%m-%d')
    overdue = [loan for loan in loans if loan['ReturnDate'] == '' and loan['DueDate'] < today]
    if overdue:
        print("\nOverdue Loans:")
        for loan in overdue:
            print(f"Loan ID: {loan['LoanID']} | ISBN: {loan['ISBN']} | Due: {loan['DueDate']}")
    else:
        print("No overdue loans.")

def reset_member_password():
    members = load_csv('members.csv')
    member_id = input("Enter Member ID to reset password: ")
    for member in members:
        if member['MemberID'] == member_id:
            new_password = input("Enter new password: ")
            hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            member['PasswordHash'] = hashed_password
            save_csv('members.csv', members, members[0].keys())
            print(f"Password for member {member['Name']} has been reset.")
            return
    print("Member ID not found.")

# === Main Entry ===
def main():
    main_menu()

if __name__ == "__main__":
    main()
