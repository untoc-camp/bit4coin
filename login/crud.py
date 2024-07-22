from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate

#from passlib.context import CryptContext
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#def get_password_hash(password):
#    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    db_user = User(
        user_name=user.user_name,
        email=user.email,
        password=user.password,
        api_key=user.api_key,
        api_key_secret=user.api_key_secret
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user