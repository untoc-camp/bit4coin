from sqlalchemy.orm import Session
from models import User
from user_schema import UserCreate

#password 암호화 함수입니다. 사용 시에 정보 관리가 힘들 것 같아 일단 주석 처리했습니다.
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