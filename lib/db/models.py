from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()

engine = create_engine('sqlite:///libmate.db')
Session = sessionmaker(bind=engine)
session = Session()

class Author(Base):
    __tablename__ = 'authors' #define the table name
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)#author name must be unique and cannot be null
    books = relationship('Book', back_populates='author', cascade="all, delete-orphan") # define a relationship with the Book model
    # cascade="all, delete-orphan" ensures that when an author is deleted, all their books are also deleted
    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"
    
class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False) #genre name must be unique and cannot be null
    books = relationship('Book', back_populates='genre') # define a relationship with the Book model
    def __repr__(self):
        return f"<Genre(id={self.id}, name='{self.name}')>"
    
class Book(Base):
    __tablename__ = 'books' 
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False) # book title cannot be null
    published_year = Column(Integer)

    # foreign keys to the authors and genres tables
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False) #foreign key to the authors table
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False) 

    # define the relationships
    author = relationship('Author', back_populates='books') 
    genre = relationship('Genre', back_populates='books') 
    loans = relationship('Loan', back_populates='book') 
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', " \
               f"author_id={self.author_id}, genre_id={self.genre_id})>"
    
class Borrower(Base):
    __tablename__ = 'borrowers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)# phone number must be unique
    loans = relationship('Loan', back_populates='borrower', cascade="all, delete-orphan")
    def __repr__(self):
        return f"<Borrower(id={self.id}, name='{self.name}', phone_number='{self.phone_number}')>"
        
class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    loan_date = Column(String, nullable=False)
    return_date= Column(String, nullable=True)
    borrower_id = Column(Integer, ForeignKey('borrowers.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrower = relationship('Borrower', back_populates='loans')
    book = relationship('Book', back_populates='loans')
    def __repr__(self):
        return f"<Loan(id={self.id}, loan_date='{self.loan_date}', " \
               f"borrower_id={self.borrower_id}, book_id={self.book_id})>"