from fastapi import FastAPI, Request, Depends, HTTPException,Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from schemas import UserCreate, UserResponse, Userlogin
from models import User
from crud import create_user

import models

app = FastAPI()

# 정적 파일 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 의존성 주입
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("login.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.get("/signin_page", response_class=HTMLResponse)
async def read_root():
    with open("signin.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.get("/more", response_class=HTMLResponse)
async def read_root():
    with open("more.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    db_user_nickname = db.query(User).filter(User.user_name == user.user_name).first()
    if db_user:
        raise HTTPException(status_code=400, detail="이미 가입한 이메일이 존재합니다.")
    if db_user_nickname:
        raise HTTPException(status_code=400, detail="이미 같은 id가 존재합니다.")
    new_user = create_user(db=db, user=user)
    return new_user


@app.post("/login" ,response_class=HTMLResponse)
async def login_form(user: Userlogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.user_name == user.user_name_login).first()
    
    if db_user :
        if db_user.password == user.password_login :
            return "로그인 성공"
        else :
            raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다")
    else :
        raise HTTPException(status_code=400, detail="id가 존재하지 않습니다")
