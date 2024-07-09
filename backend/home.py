from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from strategys.init import binance
from strategys.position import enter_position, exit_position
from strategys.function import get_cur_price, get_balance, dataFrame, calAmount, VolatilityBreakout, get_symbol_info
from strategys.env import profit_percent, loss_percent, purchase_percent, con_diffma40_4, timeframe, symbols, k
from strategys.strategy import strategy_1, strategy_2, strategy_3
import subprocess
import time

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add CORS middleware
origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def init(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/enter_position", response_class=HTMLResponse)
async def enter_position(request: Request, symbol: str = Form(...), purchase_percent: float = Form(...), leverage: int = Form(...), strategys:str = Form(...)):
    if strategys == "strategy_1":
        strategy_1(symbol, purchase_percent, leverage)
    elif strategys == "strategy_2":
        strategy_2(symbol, purchase_percent, leverage)
    elif strategys == "strategy_3":
        strategy_3(symbol, purchase_percent, leverage)
        
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/goto", response_class=HTMLResponse)
async def goto(request: Request):
    return templates.TemplateResponse("goto.html", {"request": request})

@app.get("/symbols_info", response_class=HTMLResponse)
async def symbols_info(request: Request):
    return templates.TemplateResponse("symbols_info.html", {"request": request})

@app.get("/history", response_class=HTMLResponse)
def history(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

@app.get("/mypage", response_class=HTMLResponse)
def mypage(request: Request):
    return templates.TemplateResponse("mypage.html", {"request": request})

