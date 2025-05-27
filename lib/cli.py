# This script provides a simple CLI to interact with the library database.
import os
import sys
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Ensure the current directory is in the path 

from lib.db.models import Author, Genre, Book, Borrower, Loan, session

def list_all_authors():
    """List all authors in the database."""
    authors = session.query(Author).all()
    if authors:
         print("\n--- All Authors ---")
         for author in authors:
            print(f"ID: {author.id}, Name: {author.name}")
    else:
        print("\nNo authors found in the library.")

def list_all_genres():
    """List all genres in the database."""
    genres = session.query(Genre).all()
    if genres:
        print("\n--- All Genres ---")
        for genre in genres:
            print(f"ID: {genre.id}, Name: {genre.name}")
    else:
        print("\nNo genres found in the library.")

def list_all_books():
    """List all books with their author and genre."""
    books = session.query(Book).all()
    if books:
        print("\n--- All Books ---")
        for book in books:
            author_name = book.author.name if book.author else "N/A"
            genre_name = book.genre.name if book.genre else "N/A"
            print(f"ID: {book.id}, Title: '{book.title}', Author: '{author_name}', Genre: '{genre_name}'")
    else:
        print("\nNo books found in the library.")

def list_all_borrowers():
    """List all borrowers."""
    borrowers = session.query(Borrower).all()
    if borrowers:
        print("\n--- All Borrowers ---")
        for borrower in borrowers:
            print(f"ID: {borrower.id}, Name: '{borrower.name}', Phone: '{borrower.phone_number}'")
    else:
        print("\nNo borrowers found.")
def add_author():
    """Add a new author to the database."""
    print("\n--- Add New Author ---")
    name = input("Enter author's name: ").strip()  # Get author name from user input
    # Validate input
    if not name:
        print("Author name cannot be empty.")
        return
    # Check if author already exists
    existing_author = session.query(Author).filter_by(name=name).first()
    if existing_author:
        print(f"Author '{name}' already exists with ID {existing_author.id}.")
        return
    try:
        new_author = Author(name=name)  # Create a new Author instance
        session.add(new_author)  # Add the new author to the session
        session.commit()  # Commit the transaction
        print(f"Author '{new_author.name}' added with ID {new_author.id}.")
    except Exception as e:
        session.rollback()# Rollback the session in case of error
        print(f"Error adding author: {e}")
#  This function adds a new author to the database, ensuring the name is unique and not empty.
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

# This function adds a new borrower to the database, ensuring the phone number is unique and not empty.
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

# This function finds books by title, allowing for case-insensitive and partial matches.
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


# This function finds a borrower by their phone number, displaying their details and any active loans.
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
            print("--- Active Loans ---")
            for loan in borrower.loans:
                status = "Returned" if loan.return_date else "Outstanding"
                print(f"  - Book: '{loan.book.title}', Loaned: {loan.loan_date}, Status: {status}")
        else:
            print("  No loans for this borrower.")
    else:
        print(f"\nNo borrower found with phone number '{phone_number}'.")

# This function displays the main menu options for the CLI.
def display_menu():
    """Displays the main menu options."""
    print("\n--- LibMate Manager CLI ---")
    print("--- View Data ---")
    print("1. List All Authors")
    print("2. List All Genres")
    print("3. List All Books")
    print("4. List All Borrowers")
    print("--- Add New Data ---")
    print("5. Add New Author")
    print("6. Add New Book")
    print("7. Add New Borrower")
    print("--- Find Data ---")
    print("8. Find Book by Title")
    print("9. Find Borrower by Phone Number")
    print("--- Other ---")
    print("10. Exit")
    print("---------------------------")

# This is the main function that runs the CLI, displaying the menu and handling user input.
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
            add_author()
        elif choice == '6':
            add_book()
        elif choice == '7':
            add_borrower()
        elif choice == '8':
            find_book_by_title()
        elif choice == '9':
            find_borrower_by_phone()
        elif choice == '10':
            print("Exiting LibMate Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

        input("\nPress Enter to continue...") # Pause for user to read output

    session.close() # Close the session when the application exits

if __name__ == '__main__':
    main()