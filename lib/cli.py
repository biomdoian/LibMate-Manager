# This script provides a simple CLI to interact with the library database.
import os
import sys
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

def display_menu():
    """Display the main menu."""
    print("\n--- Library Management CLI ---")
    print("1. List All Authors")
    print("2. List All Genres")
    print("3. List All Books")
    print("4. List All Borrowers")
    print("5. Exit")
    print("----------------------------")

def main():
    """Main function to run the CLI."""
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            list_all_authors()
        elif choice == '2':
            list_all_genres()
        elif choice == '3':
            list_all_books()
        elif choice == '4':
            list_all_borrowers()
        elif choice == '5':
            print("Exiting LibMate Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")  # Pause for user to read output
    session.close()  # Close the session when application exits
if __name__ == "__main__":
    main()
