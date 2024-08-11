from pydantic import BaseModel, UUID4
from datetime import datetime

class MessageBase(BaseModel):
    id:str
    chat_id: str
    sender_id: str
    receptor_id :str
    content_text: str

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content_text: str

class MessageSchema(MessageBase):
    id: str
    created_datetime: datetime
    updated_datetime: datetime


class CreateMessage(BaseModel):
    chat_id:str
    sender_id: str
    receptor_id :str
    content_text: str
    created_datetime: datetime