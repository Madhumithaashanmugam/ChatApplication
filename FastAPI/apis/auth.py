from fastapi import APIRouter,Depends,Body,HTTPException,status
from typing import Dict
from sqlalchemy.orm import Session
from services.auth import authenticate_user,create_access_token,timedelta,Annotated,get_current_user
from models.users.schema import TokenData,UserDetails,Data
from models.users.models import User
from config.db.session import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from services.execption_service import AppException

auth_router = APIRouter(tags=["Auth"])

import logging

logger = logging.getLogger(__name__)

@auth_router.post("/account/login", response_model=TokenData)
async def login_for_access_token(data: Dict[str, str] = Body(Data), session: Session = Depends(get_db)):
    try:
        email = data.get("username")
        password = data.get("password")
        if not email or not password:
            raise HTTPException(status_code=400, detail="Username and password required")
        
        user = authenticate_user(email, password, session)
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"id": user.id, "email": user.email, "first_name": user.first_name, "last_name": user.last_name},
            expires_delta=access_token_expires
        )
        user_details = UserDetails(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        logger.info(f"User logged in: {user.id}")
        return {"access_token": access_token, "token_type": "bearer", "user": user_details}
    except HTTPException as e:
        logger.warning(f"Auth error: {str(e.detail)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected auth error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@auth_router.post("/auth/signin", response_model=TokenData)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    try:
        user = authenticate_user(form_data.username, form_data.password, session)
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"id": user.id, "email": user.email, "first_name": user.first_name, "last_name": user.last_name},
            expires_delta=access_token_expires
        )
        user_details = UserDetails(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        return {"access_token": access_token, "token_type": "bearer", "user": user_details}
    except Exception as e:
        raise AppException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@auth_router.get("/auth/signup", response_model=UserDetails)
async def read_users_me(current_user: User = Depends(get_current_user)):
    try:
        user_details = UserDetails(
            email=current_user.email,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
        )
        return user_details
    except Exception as e:
        raise AppException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))