import os
import sys
# Adds the current directory to sys.path for local imports
sys.path.append(os.getcwd())

from lib.db.models import Author, Genre, Book, Borrower, Loan, session

if __name__ == '__main__':
    print("--- Querying Database Data ---")

    # Authors
    all_authors = session.query(Author).all()
    print(f"\nTotal Authors: {len(all_authors)}")
    print("--- Authors List (ID, Name, First 3 Books) ---")
    for author in all_authors:
        book_titles = [b.title for b in author.books[:3]] # Get titles of first 3 books
        print(f"ID: {author.id}, Name: '{author.name}', Books: {book_titles if book_titles else 'None'}")

    #Genres
    all_genres = session.query(Genre).all()
    print(f"\nTotal Genres: {len(all_genres)}")
    print("--- Genres List (ID, Name) ---")
    for genre in all_genres:
        print(f"ID: {genre.id}, Name: '{genre.name}'")

    #Books
    all_books = session.query(Book).all()
    print(f"\nTotal Books: {len(all_books)}")
    print("--- Books List (ID, Title, Author, Genre) ---")
    for book in all_books[:10]: # Print details for the first 10 books
        author_name = book.author.name if book.author else "N/A"
        genre_name = book.genre.name if book.genre else "N/A"
        print(f"ID: {book.id}, Title: '{book.title}', Author: '{author_name}', Genre: '{genre_name}'")

    #Borrowers
    all_borrowers = session.query(Borrower).all()
    print(f"\nTotal Borrowers: {len(all_borrowers)}")
    print("--- Borrowers List (ID, Name, Phone Number) ---")
    for borrower in all_borrowers:
        print(f"ID: {borrower.id}, Name: '{borrower.name}', Phone: '{borrower.phone_number}'")

    #Loans
    all_loans = session.query(Loan).all()
    print(f"\nTotal Loans: {len(all_loans)}")
    print("--- Loans List (ID, Borrower, Book, Dates) ---")
    for loan in all_loans[:10]: # Print details for the first 10 loans
        borrower_name = loan.borrower.name if loan.borrower else "N/A"
        book_title = loan.book.title if loan.book else "N/A"
        print(f"Loan ID: {loan.id}, Borrower: '{borrower_name}', Book: '{book_title}', Loan Date: {loan.loan_date}, Return Date: {loan.return_date}")

    # IMPORTANT: Always close the session when done
    session.close()
    print("\nDatabase queries finished. Session closed.")
