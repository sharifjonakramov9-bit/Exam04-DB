from library.db import SessionLocal, Base, engine
from library.models import Author, Book, Student, Borrow
from library import services

Base.metadata.create_all(bind=engine)
db = SessionLocal()

author1 = services.create_author(db, "Tolstoy", "Famous Russian writer")
author2 = services.create_author(db, "Pushkin", "Russian poet")

book1 = services.create_book(db, "War and Peace", author1.id, 1869)
book2 = services.create_book(db, "Anna Karenina", author1.id, 1877)
book3 = services.create_book(db, "Eugene Onegin", author2.id, 1833)

student1 = services.create_student(db, "Ali Valiyev", "ali@mail.com")
student2 = services.create_student(db, "Olimbek", "olim@mail.com")

from datetime import datetime, timedelta
borrow1 = Borrow(student_id=student1.id, book_id=book1.id)
db.add(borrow1)
db.commit()

print("Student 1 borrow count:", services.get_student_borrow_count(db, student1.id))