from sqlalchemy.dialects.postgresql import UUID
from models.message.models import Message
from sqlalchemy.orm import Session
import uuid
from models.message.schema import MessageCreate,MessageUpdate,CreateMessage
from fastapi import Depends
from config.db.session import get_db
from .connection_manager import ConnectionManager
from models.chat.models import Chat
from models.users.models import User
manager = ConnectionManager()



def get_message(db: Session, message_id: str):
    return db.query(Message).filter(Message.id == message_id).first()

def get_messages(db: Session, chat_id: str):
    return db.query(Message).filter(Message.chat_id == chat_id).all()

async def create_message(db: Session, message: CreateMessage):
    chat = db.query(Chat).filter(Chat.id == message.chat_id).first()
    if not chat:
        raise ValueError("chat not found")
    
    
    sender_ids = [message.sender_id, message.receptor_id]
    for sender_id in sender_ids:
        if not db.query(User).filter(User.id ==sender_id).first():
            raise ValueError(f"Lead ID {sender_id} not found")
    
    db_message = Message(
        id=str(uuid.uuid4()),
        chat_id=message.chat_id,
        sender_id=message.sender_id,
        receptor_id=message.receptor_id,
        content_text=message.content_text,
        created_datetime =message.created_datetime
        
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    
    await manager.send_personal_message(message.sender_id, message.receptor_id, message.content_text)
    
    return db_message

def update_message(db: Session, message_id: str, message_update: MessageUpdate):
    db_message = get_message(db, message_id)
    if db_message:
        for key, value in message_update.model_dump().items():
            setattr(db_message, key, value)
        db.commit()
        db.refresh(db_message)
        return db_message

def delete_message(db: Session, message_id: str):
    db_message = get_message(db, message_id)
    if db_message:
        db.delete(db_message)
        db.commit()

def get_all_messages(session: Session = Depends(get_db)):
    messages = session.query(Message).all()
    return messages

def get_messages_for_user(db: Session, sender_id: str):
    return db.query(Message).filter((Message.sender_id == sender_id) | (Message.receptor_id == sender_id)).all()

