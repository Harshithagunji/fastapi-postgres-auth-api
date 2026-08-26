import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL=os.getenv('SQLALCHEMY_DATABASE_URL')

engine=create_engine(SQLALCHEMY_DATABASE_URL)

sessionlocal= sessionmaker(autoflush='False', bind=engine)

Base=declarative_base()

def get_db():
    db= sessionlocal()
    try:
        yield db
    finally:
        db.close()

def create_table():
    Base.metadata.create_all(bind=engine)