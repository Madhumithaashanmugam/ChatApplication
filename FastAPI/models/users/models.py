from sqlalchemy import Column, String, func, Enum as SQLAEnum, TIMESTAMP, text
from sqlalchemy.orm import relationship
from config.db.session import Base
import uuid
from enum import Enum

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    created_datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_datetime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
