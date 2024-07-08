from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from strategys.init import binance
from strategys.position import enter_position, exit_position
from strategys.function import get_cur_price, get_balance, dataFrame, calAmount, VolatilityBreakout, get_symbol_info
from strategys.env import profit_percent, loss_percent, purchase_percent, con_diffma40_4, timeframe, symbols, k
from strategys.strategy import strategy_1

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

@app.post("/home", response_class=HTMLResponse)
async def home(request: Request, symbol : str = Form(...), perchase_percent : str = Form(...), leverage : str = Form(...)):
    print(symbol)
    print(perchase_percent)
    print(leverage)
    return templates.TemplateResponse("home.html", {"request": request, "symbol":symbol, "perchase_percent":perchase_percent, "leverage":leverage})


@app.get("/ETC")
def ETC():
    return {"message":"ETC"}

@app.get("/symbols")
def symbols():
    return {"message":"symbols"}

@app.get("/receipt")
def receipt():
    return {"message":"receipt"}

@app.get("/mypage")
def mypage():
    return {"message":"mypage"}



