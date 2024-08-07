import re
import uuid
from passlib.context import CryptContext
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.users.models import User
from models.users.schema import CreateUser, UpdateUser
import logging

logger = logging.getLogger(__name__)

bcrypt_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")

PASSWORD_REGEX = re.compile(
    r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\*\@\#\$\!\~\^\(\)\_\-\+\=\<\>\?\;\:\'\",\`\[\]\{\}\.]).{8,12}$'
)
EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
)
PHONE_REGEX = re.compile(
    r'^\d{10}$'
)

def validate_email(email: str):
    if not EMAIL_REGEX.match(email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format."
        )
    
def validate_phone(phone: str):
    if not PHONE_REGEX.match(phone):
        raise HTTPException(
            status_code=400,
            detail="Phone number must be 10 digits long."
        )

def validate_password(password: str):
    errors = []
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter.")
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one number.")
    if not re.search(r'[\*\@\#\$\!\~\^\(\)\_\-\+\=\<\>\?\;\:\'\",\`\[\]\{\}\.]', password):
        errors.append("Password must contain at least one special character (*,@,#,$,!,~,^,(,),_,-,+,=,<,>,?,;,:,',\",`,[,],{,},.).")
    if not (8 <= len(password) <= 12):
        errors.append("Password must be between 8 and 12 characters long.")

    if errors:
        raise HTTPException(
            status_code=400,
            detail=" ".join(errors)
        )
    



def create_user(user_data: CreateUser, session: Session):
    try:
        if not re.match(r'^[a-zA-Z]+$', user_data.first_name):
            raise HTTPException(status_code=400, detail="First name must contain only letters")
        if not re.match(r'^[a-zA-Z]+$', user_data.last_name):
            raise HTTPException(status_code=400, detail="Last name must contain only letters")

        validate_email(user_data.email)
        validate_phone(user_data.phone_number)
        validate_password(user_data.hashed_password)
        
        add_user = User(
            id=str(uuid.uuid4()),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            hashed_password=bcrypt_context.hash(user_data.hashed_password),
            created_datetime=user_data.created_datetime,
            updated_datetime=user_data.updated_datetime
        )
        session.add(add_user)
        session.commit()
        session.refresh(add_user)
        logger.info(f"User created: {add_user.id}")
        return add_user
    except HTTPException as e:
        logger.error(f"Error creating user: {str(e.detail)}")



def update_user_by_id(id: str, user_data: UpdateUser, session: Session):
    user = session.get(User, id)
    if not user:
        return None
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user_by_id(id: str, session: Session):
    user = session.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}










