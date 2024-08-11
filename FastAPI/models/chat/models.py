from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
import uuid
from config.db.session import Base

class Chat(Base):
    __tablename__ = "chat"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    sender_id = Column(String, ForeignKey('user.id'), nullable=False)
    receptor_id = Column(String, ForeignKey('user.id'), nullable=False)
    created_datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")