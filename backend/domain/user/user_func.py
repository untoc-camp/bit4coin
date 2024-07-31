from fastapi import FastAPI, Request, Depends, HTTPException, Query, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from domain.user.user_schema import UserCreate, UserResponse, Userlogin, TokenData
from models import User
from domain.user.user_crud import create_user
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt
import models
from database import get_db


SECRET_KEY = "newjeans_ippuda_goat"  # 변경하세요
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 유저 인증 함수
def authenticate_user(username: str, password: str, db: Session = SessionLocal()):
    db_user = db.query(User).filter(User.user_name == username).first()
    if not db_user or db_user.password != password:
        return None
    return db_user

# JWT 토큰 생성 함수
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 토큰 검증 및 현재 유저 가져오기 함수
def get_current_user(db, token: str): #users/me direct
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        if user_name is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db_user = db.query(User).filter(User.user_name == user_name).first()#db연동필요
    if db_user is None:
        raise credentials_exception
    return User(user_name=user_name)
