
import models
from sqlalchemy.orm import Session
import schemas

def create_book(db: Session,book:schemas.BookCreate, user_id:int):
    db_book=models.Book(**book.model_dump(),owner_id=user_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db:Session, user_id:int):
    return db.query(models.Book).filter(models.Book.owner_id== user_id).all()

def get_book_by_id(db:Session, book_id: int,user_id:int):
    return db.query(models.Book).filter(models.Book.id==book_id,models.Book.owner_id==user_id).first()

def update_book(db:Session, book:schemas.BookCreate,book_id:int,user_id:int):
    book_queryset= db.query(models.Book).filter(models.Book.id==book_id,models.Book.owner_id==user_id).first()
    if book_queryset:
        for key,value in book.model_dump().items():
            setattr(book_queryset,key,value)
        db.commit()
        db.refresh(book_queryset)
    return book_queryset

def delete_book(db:Session, book_id:int,user_id:int):
    book_queryset= db.query(models.Book).filter(models.Book.id==book_id,models.Book.owner_id==user_id).first()
    if book_queryset:
        db.delete(book_queryset)
        db.commit()
    return book_queryset