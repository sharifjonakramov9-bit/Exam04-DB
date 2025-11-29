from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from .db import Base

class Author(Base):
    tablename = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    books = relationship("Book", back_populates="author")

class Book(Base):
    tablename = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))
    published_year = Column(Integer)
    isbn = Column(String(13), unique=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("Author", back_populates="books")
    borrows = relationship("Borrow", back_populates="book")

class Student(Base):
    tablename = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    grade = Column(String(20))
    registered_at = Column(DateTime, default=datetime.utcnow)

    borrows = relationship("Borrow", back_populates="student")

class Borrow(Base):
    tablename = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=14))
    returned_at = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")