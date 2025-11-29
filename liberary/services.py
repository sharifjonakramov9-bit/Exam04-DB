from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from .models import Author, Book, Student, Borrow

def get_student_borrow_count(db: Session, student_id: int) -> int:
    return db.query(func.count(Borrow.id)).filter(Borrow.student_id == student_id).scalar() or 0

def get_currently_borrowed_books(db: Session):
    return db.query(Book, Student, Borrow.borrowed_at)\
        .join(Borrow, Borrow.book_id==Book.id)\
        .join(Student, Student.id==Borrow.student_id)\
        .filter(Borrow.returned_at.is_(None))\
        .all()

def get_books_by_author(db: Session, author_id: int):
    return db.query(Book).filter(Book.author_id==author_id).all()

def get_overdue_borrows(db: Session):
    now = datetime.utcnow()
    rows = db.query(Borrow, Student, Book)\
        .join(Student, Student.id==Borrow.student_id)\
        .join(Book, Book.id==Borrow.book_id)\
        .filter(Borrow.returned_at.is_(None))\
        .filter(Borrow.due_date < now)\
        .all()
    results = []
    for borrow, student, book in rows:
        overdue_days = (now - borrow.due_date).days
        results.append((borrow, student, book, overdue_days))
    return results