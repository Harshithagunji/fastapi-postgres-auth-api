
from db import Base
from sqlalchemy import Integer, Column,String, ForeignKey
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__='Books'

    id= Column(Integer, primary_key=True, index=True)
    title= Column(String, index= True)
    description= Column(String, index= True)
    author= Column(String, index= True)
    year= Column(Integer)
    owner_id= Column(Integer, ForeignKey('users.id'))
    owner= relationship('User',back_populates='books')

class User(Base):
    __tablename__='users'
    id= Column(Integer, primary_key=True,index= True)
    username=Column(String,unique=True,index= True)
    hashed_password=Column(String)
    books=relationship('Book',back_populates='owner')
