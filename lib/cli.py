import os
import sys
import datetime

# Ensure the project root is in the path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.db.models import Author, Genre, Book, Borrower, Loan, session


#Views the Data Functions
def list_all_authors():
    """Lists all authors in the database."""
    authors = session.query(Author).all()
    if authors:
        print("\n--- All Authors ---")
        for author in authors:
            print(f"ID: {author.id}, Name: {author.name}")
    else:
        print("\nNo authors found in the library.")

#List All Genres Function 
def list_all_genres():
    """Lists all genres in the database."""
    genres = session.query(Genre).all()
    if genres:
        print("\n--- All Genres ---")
        for genre in genres:
            print(f"ID: {genre.id}, Name: {genre.name}")
    else:
        print("\nNo genres found in the library.")

# List All Books Function
def list_all_books():
    """Lists all books with their author and genre."""
    books = session.query(Book).all()
    if books:
        print("\n--- All Books ---")
        for book in books:
            author_name = book.author.name if book.author else "N/A"
            genre_name = book.genre.name if book.genre else "N/A"
            # Check for existing outstanding loans
            outstanding_loans = session.query(Loan).filter(
                Loan.book_id == book.id,
                Loan.return_date == None # Check for null return_date
            ).count()
            status = "Available" if outstanding_loans == 0 else "On Loan"
            print(f"ID: {book.id}, Title: '{book.title}', Published Year: {book.published_year}, Author: '{author_name}', Genre: '{genre_name}', Status: {status}")
    else:
        print("\nNo books found in the library.")

# List All Borrowers Function
def list_all_borrowers():
    """Lists all borrowers."""
    borrowers = session.query(Borrower).all()
    if borrowers:
        print("\n--- All Borrowers ---")
        for borrower in borrowers:
            print(f"ID: {borrower.id}, Name: '{borrower.name}', Phone: '{borrower.phone_number}'")
    else:
        print("\nNo borrowers found.")

# List All Loans Function
def list_all_loans():
    """Lists all loans with borrower and book details."""
    loans = session.query(Loan).all()
    if loans:
        print("\n--- All Loans ---")
        for loan in loans:
            borrower_name = loan.borrower.name if loan.borrower else "N/A"
            book_title = loan.book.title if loan.book else "N/A"
            status = "Returned" if loan.return_date else "Outstanding"
            print(f"Loan ID: {loan.id}, Borrower: '{borrower_name}', Book: '{book_title}', Loan Date: {loan.loan_date}, Return Date: {loan.return_date if loan.return_date else 'N/A'} (Status: {status})")
    else:
        print("\nNo loan records found.")

#Add Data Functions

def add_author():
    """Adds a new author to the database."""
    print("\n--- Add New Author ---")
    name = input("Enter author's name: ").strip()
    if not name:
        print("Author name cannot be empty.")
        return

    # Check if author already exists
    existing_author = session.query(Author).filter_by(name=name).first()
    if existing_author:
        print(f"Author '{name}' already exists with ID: {existing_author.id}.")
        return

    try:
        new_author = Author(name=name)
        session.add(new_author)
        session.commit()
        print(f"Author '{new_author.name}' added with ID: {new_author.id}.")
    except Exception as e:
        session.rollback() # Rollback in case of error
        print(f"Error adding author: {e}")

# Add Book Function
def add_book():
    """Adds a new book to the database."""
    print("\n--- Add New Book ---")
    title = input("Enter book title: ").strip()
    if not title:
        print("Book title cannot be empty.")
        return

    published_year_str = input("Enter published year (e.g., 2023): ").strip()
    try:
        published_year = int(published_year_str)
    except ValueError:
        print("Invalid year. Please enter a number.")
        return

    # Select Author
    list_all_authors()
    author_id_str = input("Enter Author ID for the book: ").strip()
    try:
        author_id = int(author_id_str)
        author = session.query(Author).get(author_id)
        if not author:
            print(f"Author with ID {author_id} not found.")
            return
    except ValueError:
        print("Invalid Author ID. Please enter a number.")
        return

    # Select Genre
    list_all_genres()
    genre_id_str = input("Enter Genre ID for the book: ").strip()
    try:
        genre_id = int(genre_id_str)
        genre = session.query(Genre).get(genre_id)
        if not genre:
            print(f"Genre with ID {genre_id} not found.")
            return
    except ValueError:
        print("Invalid Genre ID. Please enter a number.")
        return

    try:
        new_book = Book(
            title=title,
            published_year=published_year,
            author=author,
            genre=genre
        )
        session.add(new_book)
        session.commit()
        print(f"Book '{new_book.title}' by {new_book.author.name} added with ID: {new_book.id}.")
    except Exception as e:
        session.rollback()
        print(f"Error adding book: {e}")

# Add Borrower Function
def add_borrower():
    """Adds a new borrower to the database."""
    print("\n--- Add New Borrower ---")
    name = input("Enter borrower's name: ").strip()
    if not name:
        print("Borrower name cannot be empty.")
        return

    phone_number = input("Enter borrower's phone number (must be unique): ").strip()
    if not phone_number:
        print("Phone number cannot be empty.")
        return

    # Check if phone number already exists
    existing_borrower = session.query(Borrower).filter_by(phone_number=phone_number).first()
    if existing_borrower:
        print(f"Borrower with phone number '{phone_number}' already exists (ID: {existing_borrower.id}).")
        return

    try:
        new_borrower = Borrower(name=name, phone_number=phone_number)
        session.add(new_borrower)
        session.commit()
        print(f"Borrower '{new_borrower.name}' added with ID: {new_borrower.id}.")
    except Exception as e:
        session.rollback()
        print(f"Error adding borrower: {e}")

# Delete Data Functions

def delete_author():
    """Deletes an author and cascades to their books."""
    print("\n--- Delete Author ---")
    list_all_authors()
    author_id_str = input("Enter Author ID to delete: ").strip()
    try:
        author_id = int(author_id_str)
        author_to_delete = session.query(Author).get(author_id)
        if not author_to_delete:
            print(f"Author with ID {author_id} not found.")
            return
    except ValueError:
        print("Invalid Author ID. Please enter a number.")
        return

    confirm = input(f"Are you sure you want to delete '{author_to_delete.name}' (ID: {author_to_delete.id}) and ALL their books? (yes/no): ").lower().strip()
    if confirm == 'yes':
        try:
            session.delete(author_to_delete)
            session.commit()
            print(f"Author '{author_to_delete.name}' and all their books deleted successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting author: {e}")
    else:
        print("Author deletion cancelled.")
 
 # Delete Book Function
def delete_book():
    """Deletes a book."""
    print("\n--- Delete Book ---")
    list_all_books()
    book_id_str = input("Enter Book ID to delete: ").strip()
    try:
        book_id = int(book_id_str)
        book_to_delete = session.query(Book).get(book_id)
        if not book_to_delete:
            print(f"Book with ID {book_id} not found.")
            return
    except ValueError:
        print("Invalid Book ID. Please enter a number.")
        return

    # Check for outstanding loans before deleting book
    outstanding_loans_for_book = session.query(Loan).filter(
        Loan.book_id == book_to_delete.id,
        Loan.return_date == None
    ).first()

    if outstanding_loans_for_book:
        print(f"Cannot delete book '{book_to_delete.title}' (ID: {book_to_delete.id}) because it has an outstanding loan (Loan ID: {outstanding_loans_for_book.id}). Please return the book first.")
        return

    confirm = input(f"Are you sure you want to delete '{book_to_delete.title}' (ID: {book_to_delete.id})? (yes/no): ").lower().strip()
    if confirm == 'yes':
        try:
            session.delete(book_to_delete)
            session.commit()
            print(f"Book '{book_to_delete.title}' deleted successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting book: {e}")
    else:
        print("Book deletion cancelled.")


# Delete Borrower Function
def delete_borrower():
    """Deletes a borrower and cascades to their loans."""
    print("\n--- Delete Borrower ---")
    list_all_borrowers()
    borrower_id_str = input("Enter Borrower ID to delete: ").strip()
    try:
        borrower_id = int(borrower_id_str)
        borrower_to_delete = session.query(Borrower).get(borrower_id)
        if not borrower_to_delete:
            print(f"Borrower with ID {borrower_id} not found.")
            return
    except ValueError:
        print("Invalid Borrower ID. Please enter a number.")
        return

    confirm = input(f"Are you sure you want to delete '{borrower_to_delete.name}' (ID: {borrower_to_delete.id}) and ALL their loan records? (yes/no): ").lower().strip()
    if confirm == 'yes':
        try:
            session.delete(borrower_to_delete)
            session.commit()
            print(f"Borrower '{borrower_to_delete.name}' and all their loan records deleted successfully.")
        except Exception as e:
            session.rollback()
            print(f"Error deleting borrower: {e}")
    else:
        print("Borrower deletion cancelled.")

# Find Data Functions

def find_book_by_title():
    """Finds books by title (case-insensitive, partial match)."""
    print("\n--- Find Book by Title ---")
    search_term = input("Enter part of the book title to search for: ").strip()
    if not search_term:
        print("Search term cannot be empty.")
        return

    # Using ilike for case-insensitive partial match
    books = session.query(Book).filter(Book.title.ilike(f'%{search_term}%')).all()
    if books:
        print(f"\n--- Books matching '{search_term}' ---")
        for book in books:
            author_name = book.author.name if book.author else "N/A"
            genre_name = book.genre.name if book.genre else "N/A"
            print(f"ID: {book.id}, Title: '{book.title}', Author: '{author_name}', Genre: '{genre_name}'")
    else:
        print(f"\nNo books found matching '{search_term}'.")

# Find Borrower by Phone Number Function
def find_borrower_by_phone():
    """Finds a borrower by phone number."""
    print("\n--- Find Borrower by Phone Number ---")
    phone_number = input("Enter borrower's phone number: ").strip()
    if not phone_number:
        print("Phone number cannot be empty.")
        return

    borrower = session.query(Borrower).filter_by(phone_number=phone_number).first()
    if borrower:
        print(f"\n--- Borrower Found ---")
        print(f"ID: {borrower.id}, Name: '{borrower.name}', Phone: '{borrower.phone_number}'")
        # Optionally show their loans
        if borrower.loans:
            print("--- Loans for this Borrower ---")
            for loan in borrower.loans:
                status = "Returned" if loan.return_date else "Outstanding"
                print(f"  - Book: '{loan.book.title}', Loaned: {loan.loan_date}, Returned: {loan.return_date if loan.return_date else 'N/A'} (Status: {status})")
        else:
            print("  No loans for this borrower.")
    else:
        print(f"\nNo borrower found with phone number '{phone_number}'.")

# Loan Management Functions

def borrow_book():
    """Records a new loan (borrowing a book)."""
    print("\n--- Borrow a Book ---")

    # Step 1: Select Borrower
    list_all_borrowers()
    borrower_id_str = input("Enter Borrower ID: ").strip()
    try:
        borrower_id = int(borrower_id_str)
        borrower = session.query(Borrower).get(borrower_id)
        if not borrower:
            print(f"Borrower with ID {borrower_id} not found.")
            return
    except ValueError:
        print("Invalid Borrower ID. Please enter a number.")
        return

    # Step 2: Select Book
    list_all_books() # This now shows book status (Available/On Loan)
    book_id_str = input("Enter Book ID to borrow: ").strip()
    try:
        book_id = int(book_id_str)
        book = session.query(Book).get(book_id)
        if not book:
            print(f"Book with ID {book_id} not found.")
            return
    except ValueError:
        print("Invalid Book ID. Please enter a number.")
        return

    # Step 3: Check if the book is already on loan
    # Look for an outstanding loan for this book
    outstanding_loan = session.query(Loan).filter(
        Loan.book_id == book.id,
        Loan.return_date == None
    ).first()

    if outstanding_loan:
        print(f"Book '{book.title}' is currently on loan (Loan ID: {outstanding_loan.id}) and cannot be borrowed.")
        return

    # Step 4: Create the loan record
    loan_date = datetime.date.today().isoformat() # Current date as string

    try:
        new_loan = Loan(
            borrower=borrower,
            book=book,
            loan_date=loan_date,
            return_date=None # It's a new loan, so no return date yet
        )
        session.add(new_loan)
        session.commit()
        print(f"Book '{book.title}' successfully borrowed by '{borrower.name}'. Loan ID: {new_loan.id}.")
    except Exception as e:
        session.rollback()
        print(f"Error borrowing book: {e}")

# Return Book Function
def return_book():
    """Records the return of a book."""
    print("\n--- Return a Book ---")

    # Step 1: List all outstanding loans
    outstanding_loans = session.query(Loan).filter(Loan.return_date == None).all()
    if not outstanding_loans:
        print("\nNo outstanding loans to return.")
        return

    print("\n--- Outstanding Loans ---")
    for loan in outstanding_loans:
        borrower_name = loan.borrower.name if loan.borrower else "N/A"
        book_title = loan.book.title if loan.book else "N/A"
        print(f"Loan ID: {loan.id}, Book: '{book_title}', Borrower: '{borrower_name}', Loan Date: {loan.loan_date}")

    # Step 2: Select loan to return
    loan_id_str = input("Enter Loan ID to mark as returned: ").strip()
    try:
        loan_id = int(loan_id_str)
        loan_to_return = session.query(Loan).get(loan_id)
        if not loan_to_return:
            print(f"Loan with ID {loan_id} not found.")
            return
    except ValueError:
        print("Invalid Loan ID. Please enter a number.")
        return

    if loan_to_return.return_date:
        print(f"Loan ID {loan_to_return.id} (Book: '{loan_to_return.book.title}') has already been returned on {loan_to_return.return_date}.")
        return

    # Step 3: Update the loan record with return date
    return_date = datetime.date.today().isoformat() # Current date as string
    try:
        loan_to_return.return_date = return_date
        session.commit()
        print(f"Book '{loan_to_return.book.title}' successfully returned by '{loan_to_return.borrower.name}'. Marked as returned on {return_date}.")
    except Exception as e:
        session.rollback()
        print(f"Error returning book: {e}")


# CLI Menu and Main Loop

def display_menu():
    """Displays the main menu options."""
    print("\n--- LibMate Manager CLI ---")
    print("--- View Data ---")
    print("1. List All Authors")
    print("2. List All Genres")
    print("3. List All Books")
    print("4. List All Borrowers")
    print("5. List All Loans")
    print("--- Add New Data ---")
    print("6. Add New Author")
    print("7. Add New Book")
    print("8. Add New Borrower")
    print("--- Delete Data ---")
    print("9. Delete Author")
    print("10. Delete Book")
    print("11. Delete Borrower")
    print("--- Find Data ---")
    print("12. Find Book by Title")
    print("13. Find Borrower by Phone Number")
    print("--- Loan Management ---")
    print("14. Borrow a Book")
    print("15. Return a Book")
    print("--- Other ---")
    print("16. Exit") 
    print("---------------------------")


def main():
    """Main function to run the CLI."""
    while True:
        display_menu()
        choice = input("Enter your choice: ").strip() # .strip() removes whitespace

        if choice == '1':
            list_all_authors()
        elif choice == '2':
            list_all_genres()
        elif choice == '3':
            list_all_books()
        elif choice == '4':
            list_all_borrowers()
        elif choice == '5':
            list_all_loans()
        elif choice == '6':
            add_author()
        elif choice == '7':
            add_book()
        elif choice == '8':
            add_borrower()
        elif choice == '9':
            delete_author()
        elif choice == '10':
            delete_book()
        elif choice == '11':
            delete_borrower()
        elif choice == '12':
            find_book_by_title()
        elif choice == '13':
            find_borrower_by_phone()
        elif choice == '14':
            borrow_book()
        elif choice == '15':
            return_book()
        elif choice == '16':
            print("Exiting LibMate Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...") # Pause for user to read output

    session.close() # Close the session when the application exits

if __name__ == '__main__':
    main()