# from sqlalchemy.orm import Session
# from models.chat.models import Chat
# from models.chat.schema import CreateMessage, UpdateMessage, ViewMessage

# def create_message(db: Session, message_data: CreateMessage) -> Chat:
#     db_message = Chat(**message_data.dict())
#     db.add(db_message)
#     db.commit()
#     db.refresh(db_message)
#     return db_message

# def get_messages(db: Session, sender_id: int, receptor_id: int):
#     return db.query(Chat).filter(
#         (Chat.sender_id == sender_id) & (Chat.receptor_id == receptor_id) |
#         (Chat.sender_id == receptor_id) & (Chat.receptor_id == sender_id)
#     ).all()

# def update_message(db: Session, message_id: str, message_data: UpdateMessage):
#     db_message = db.query(Chat).filter(Chat.id == message_id).first()
#     if db_message:
#         for key, value in message_data.dict().items():
#             if value is not None:
#                 setattr(db_message, key, value)
#         db.commit()
#         db.refresh(db_message)
#     return db_message

# def delete_message(db: Session, message_id: str):
#     db_message = db.query(Chat).filter(Chat.id == message_id).first()
#     if db_message:
#         db.delete(db_message)
#         db.commit()
#     return db_message
from sqlalchemy.orm import Session
from models.chat.models import Chat
import uuid
from sqlalchemy.sql import func
from config.db.session import get_db
from fastapi import Depends



def create_chat(db: Session, sender_id: str, receptor_id: str):
    chat = Chat(
        id=str(uuid.uuid4()),
        sender_id=sender_id,
        receptor_id = receptor_id,
        created_datetime=func.now()
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def get_chat(db: Session, chat_id: str):
    return db.query(Chat).filter(Chat.id == chat_id).first()



def delete_chat(db: Session, chat_id: str):
    db_chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if db_chat:
        db.delete(db_chat)
        db.commit()



def get_all_chats(session: Session = Depends(get_db)):
    chats = session.query(Chat).all()
    return chats

