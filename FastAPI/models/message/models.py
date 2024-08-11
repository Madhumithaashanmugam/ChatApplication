from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from config.db.session import Base

class Message(Base):
    __tablename__ = "message"

    id = Column(String, primary_key=True, unique=True, default=lambda: str(uuid.uuid4()))
    chat_id = Column(String, ForeignKey("chat.id"), nullable=False)
    sender_id = Column(String, ForeignKey("user.id"), nullable=False)
    receptor_id = Column(String, ForeignKey("user.id"), nullable=False)
    content_text = Column(String)
    created_datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    chat = relationship("Chat", back_populates="messages")