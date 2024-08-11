from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.chat.schema import Chat_schema,ChatCreate
from typing import List
from services import chat_service
from config.db.session import get_db
from starlette import status

chat_api = APIRouter(tags=["chat"])

@chat_api.post("/chats/", response_model=Chat_schema)
def create_chat_endpoint(chat: ChatCreate, db: Session = Depends(get_db)):
    return chat_service.create_chat(db=db, sender_id=chat.sender_id, receptor_id= chat.receptor_id)

@chat_api.get("/chats/{chat_id}", response_model=Chat_schema)
def read_chat(chat_id: str, db: Session = Depends(get_db)):
    db_chat = chat_service.get_chat(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=404, detail="chat not found")
    return db_chat

@chat_api.delete("/chats/{chat_id}")
def delete_chat_endpoint(chat_id: str, db: Session = Depends(get_db)):
    chat_service.delete_chat(db=db, chat_id=chat_id)
    return {"message": "chat deleted successfully"}


@chat_api.get("/chats", response_model=List[Chat_schema], status_code=status.HTTP_200_OK)
def get_all_chats_api(session: Session = Depends(get_db)):
    chats = chat_service.get_all_chats(session)
    return chats