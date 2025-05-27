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
    books = relationship('Book', back_populates='author')# define a relationship with the Book model
    def __repr__(self):
        return f"<Author(id={self.id}, name='{self.name}')>"