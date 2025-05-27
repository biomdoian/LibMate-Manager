import os
import sys
sys.path.append(os.getcwd())  # Ensure the current directory is in the path
from faker import Faker #Faker is a library that generates fake data
import random
import datetime

from lib.db.models import Author, Genre, Book, Borrower, Loan, session, engine, Base

if __name__ == '__main__':
    print("Recreating database tables...")
    # Drop all tables and recreate them
    Base.metadata.drop_all(engine)  
    Base.metadata.create_all(engine)  
    print("Database tables recreated.")

    fake = Faker()  # Create a Faker instance
       # Generate fake data for authors, genres, books, borrowers, and loans
    print("creating authors...")
    authors = []
    for _ in range(10): # Generate 10 authors
        author = Author(name=fake.name())
        session.add(author)
        authors.append(author)
    session.commit()  # Commit authors to get their IDs

    print("Creating genres...")
    genres = []
    genre_names = ['Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Biography', 'Thriller', 'History', 'poetry']
    for name in genre_names:
        genre = Genre(name=name)
        session.add(genre)
        genres.append(genre)
    session.commit()  

    print("Creating books...")
    books = []
    for _ in range(50):
        book = Book(
            title=fake.catch_phrase(),  # Generate a random book title
            published_year=random.randint(1900, 2023),
            author=random.choice(authors),  
            genre=random.choice(genres)  
        )
        session.add(book)
        books.append(book)
    session.commit()  

    print("Creating borrowers...")
    borrowers = []
    for _ in range(15):
        borrower = Borrower(
            name=fake.name(),
            phone_number=fake.phone_number()
        )
        session.add(borrower)
        borrowers.append(borrower)
    session.commit()

    print("create loans...")
    loans = []
    for _ in range(30):
        loan_date_obj= fake.date_this_year()
        loan_date_str = loan_date_obj.isoformat()
        return_date_str = None
        if random.random() > 0.3:
            delta_days = random.randint(1, 60)  # Randomly choose a return date within 30 days
            return_date_obj = loan_date_obj + datetime.timedelta(days=delta_days)
            # Convert to string format for storing in the database
            return_date_str = return_date_obj.isoformat()

        loan = Loan(
            borrower=random.choice(borrowers),  # Randomly select a borrower
            book=random.choice(books),
            loan_date=loan_date_str,
            return_date=return_date_str  # Use the formatted return date or None if not returned
        )
        session.add(loan)
        loans.append(loan)
    session.commit()

    session.close()  # Close the session
    print("Database seeded with data successfully!")  # Confirmation message
 

        