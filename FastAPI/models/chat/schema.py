from pydantic import BaseModel
from datetime import datetime

class ChatBase(BaseModel):
    sender_id: str
    receptor_id:str

class ChatCreate(ChatBase):
    pass 

class Chat_schema(ChatBase):
    id: str
    created_datetime: datetime