
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import session
from db import get_db
import models
import os
from dotenv import load_dotenv

SECRET_KEY= os.getenv('SECRET_KEY')
ALGORITHM= os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES',30))

Oauth2_scheme= OAuth2PasswordBearer(tokenUrl='token')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'),hashed_password.encode('utf-8'))

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data:dict, expires_delta : timedelta|None=None):
    to_encode= data.copy()
    expire = datetime.now(timezone.utc)+ (expires_delta or timedelta(minutes=15))
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

def get_current_user(token: str= Depends(Oauth2_scheme),db: session = Depends(get_db)):
    credentials_exception= HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate':'Bearer'}
   )
    try: 
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username:str=payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.username== username).first()

    if user is None:
        raise credentials_exception
    return user
