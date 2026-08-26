
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import schemas, models, services
from db import get_db, engine
from sqlalchemy.orm import Session
import auth

models.Base.metadata.create_all(bind=engine)

app= FastAPI()


#===============Authentication and user endpoints ==========================

@app.post('/register', status_code=status.HTTP_201_CREATED)

def register_user(username:str, password:str, db: Session=Depends(get_db)):
    existing_user= db.query(models.User).filter(models.User.username==username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already existed')
    hashed_pass= auth.get_password_hash(password)
    new_user=models.User(username=username,hashed_password=hashed_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return{'message':'User registered successfully'}

@app.post('/token')
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user= db.query(models.User).filter(models.User.username== form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'www-authenticate':'Bearer'}
        )
    access_token_expires= timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=auth.create_access_token(
        data={'sub':user.username},expires_delta= access_token_expires
    )
    return{'access_token': access_token, 'token_type':'bearer'}


#=============CRUD  Endpoints===========================

@app.get('/books',response_model=list[schemas.Book])
def get_all_books(db: Session = Depends(get_db),current_user:models.User=Depends(auth.get_current_user)):
    return services.get_books(db,user_id=current_user.id)

@app.get('/books/{id}',response_model=schemas.Book)
def get_book_by_id(id:int,db: Session = Depends(get_db),current_user:models.User=Depends(auth.get_current_user)):
    book=services.get_book_by_id(db,book_id=id,user_id=current_user.id)
    if book:
        return book
    raise HTTPException(status_code=404,detail='Book not found')

@app.post('/books',response_model=schemas.Book)
def create_new_book(book: schemas.BookCreate, db: Session= Depends(get_db), 
                    current_user: models.User= Depends(auth.get_current_user)):
    return services.create_book(db, book,user_id=current_user.id)

@app.put('/books/{id}',response_model=schemas.Book)
def update_book(id:int,book:schemas.BookCreate, 
                db:Session= Depends(get_db),current_user:models.User=Depends(auth.get_current_user)):
    updated= services.update_book(db, book, book_id=id,user_id=current_user.id)
    if not updated:
        raise HTTPException(status_code=401, detail='Book not found')
    return updated

@app.delete('/books/{book_id}',response_model= schemas.Book)
def delete_book(book_id:int, db:Session=Depends(get_db),current_user: models.User= Depends(auth.get_current_user)):
    deleted= services.delete_book(db,book_id=book_id, user_id=current_user.id)
    if not deleted:
         raise HTTPException(status_code=404, detail='Book not found')
    return deleted

