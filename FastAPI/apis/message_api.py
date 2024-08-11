from fastapi import APIRouter,HTTPException,Depends
from typing import List
from services import message_service
from config.db.session import get_db
from models.message.schema import MessageCreate,MessageUpdate,MessageSchema,CreateMessage
from sqlalchemy.orm import Session
from starlette import status


message_api = APIRouter(tags=["Message"])

@message_api.post("/messages/", response_model=MessageSchema)
async def create_message_endpoint(message: CreateMessage, db: Session = Depends(get_db)):
    try:
        db_message = await message_service.create_message(db=db, message=message)
        return db_message
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@message_api.get("/messages/{message_id}", response_model=MessageSchema)
def read_message(message_id: str, db: Session = Depends(get_db)):
    db_message = message_service.get_message(db, message_id=message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@message_api.get("/messages/", response_model=list[MessageSchema])
def read_messages_chat(chat_id: str, db: Session = Depends(get_db)):
    return message_service.get_messages(db=db, chat_id=chat_id)

@message_api.put("/messages/{message_id}", response_model=MessageSchema)
def update_message_endpoint(message_id: str, message_update: MessageUpdate, db: Session = Depends(get_db)):
    db_message = message_service.update_message(db=db, message_id=message_id, message_update=message_update)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

@message_api.delete("/messages/{message_id}")
def delete_message_endpoint(message_id: str, db: Session = Depends(get_db)):
    message_service.delete_message(db=db, message_id=message_id)
    return {"message": "Message deleted successfully"}

@message_api.get("/messages", response_model=List[MessageSchema], status_code=status.HTTP_200_OK)
def get_all_messages_api(session: Session = Depends(get_db)):
    messages = message_service.get_all_messages(session)
    return messages