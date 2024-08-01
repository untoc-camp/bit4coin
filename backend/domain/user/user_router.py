from fastapi import FastAPI, Request, Depends, HTTPException, Query, status ,APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from domain.user.user_schema import UserCreate, UserResponse, Userlogin, TokenData, ChangePassword, ChangeApiKey
from models import User
from domain.user.user_crud import create_user,change_user_password
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt
import models
from database import get_db

from models import User
from domain.user.user_func import authenticate_user, create_access_token, get_current_user
router = APIRouter(
    prefix="/user",
)

SECRET_KEY = "newjeans_ippuda_goat"  # 변경하세요
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    db_user_nickname = db.query(User).filter(User.user_name == user.user_name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="이미 가입한 이메일이 존재합니다.")
    if db_user_nickname:
        raise HTTPException(status_code=400, detail="이미 같은 id가 존재합니다.")
    new_user = create_user(db=db, user=user)
    return new_user


# 로그인 엔드포인트
@router.post("/login")
async def login(user : Userlogin, db: Session = Depends(get_db)):
    user = authenticate_user(user.user_name_login, user.password_login)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 보호된 경로
@router.get("/users/me")
def read_users_me(token: str = Query(...), db: Session = Depends(get_db)):
    db_user = get_current_user(db, token=token)
    if db_user is None:
        raise HTTPException(status_coade=400, detail="Invalid token")
    return db_user

@router.post("/changepwd")
async def change(cdata : ChangePassword,  db:Session = Depends(get_db)):
    token = cdata.token
    cpwd = cdata.user_password_change
    db_user = get_current_user(db, token=token)
    if db_user is None:
        raise HTTPException(status_coade=400, detail="Invalid token")
    changed_user = change_user_password(db=db,c_user=db_user.user_name,cpwd=cpwd)
    if changed_user is None:
        raise HTTPException(status_code=1231941892397, detail="error")
    return changed_user