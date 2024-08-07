from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated,List
from uuid import UUID
from models.users.models import User
from models.users.schema import CreateUser, UpdateUser, ViewUser,UserDetails
from services import userservices
from config.db.session import get_db
from services.auth import get_current_user

user_routers = APIRouter(prefix="/users", tags=["Users"])
user_dependency = Annotated[dict, Depends(get_current_user)]

@user_routers.post("/", response_model=ViewUser)
async def create_user(user_data: CreateUser, session: Session = Depends(get_db)):
    try:
        return userservices.create_user(user_data, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_routers.get("/", response_model=List[ViewUser])
def read_all_users(user: user_dependency, session: Session = Depends(get_db)):
    query = session.query(User).all()
    return query


@user_routers.get("/{id}", response_model=ViewUser)
def read_user_by_id(user: user_dependency,id: str, session: Session = Depends(get_db)):
    try:
        user_id = str(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_routers.put("/{id}", response_model=ViewUser)
async def update_user(user: user_dependency, id: str, user_data: UpdateUser, session: Session = Depends(get_db)):
    updated_user = userservices.update_user_by_id(id, user_data, session)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@user_routers.delete("/{id}", response_model=dict)
async def delete_user(user: user_dependency, id: str, session: Session = Depends(get_db)):
    return userservices.delete_user_by_id(id, session)