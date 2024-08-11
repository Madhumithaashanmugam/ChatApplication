import uuid
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated,Dict
from passlib.context import CryptContext
from starlette import status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime,timezone
from jose import jwt, JWTError
from models.users.models import User
from models.users.schema import TokenData
from config.db.session import get_db
from dotenv import load_dotenv,find_dotenv
env_folder=find_dotenv()
load_dotenv(env_folder)
from config import ALGORITHM,SECRET_KEY



bcrypt_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/account/login')

def authenticate_user(email: str, password: str, session: Session):
    user = session.query(User).filter(User.email == email).first()
    if not user or not bcrypt_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return user




def create_access_token(data: Dict[str, str], expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.now(timezone.utc) + expires_delta})
    else:
        to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=15)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_bearer), session: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        user = session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
