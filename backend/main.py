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
file_name = "main"



@app.get("/", response_class=HTMLResponse)
async def init(request: Request):
    return templates.TemplateResponse(f"{file_name}.html", {"request": request})

@app.get("/hello")
def hello():
    return {"message":"hello"}

@app.get("/markets", response_class=HTMLResponse)
async def get_markets(request: Request):
    markets = binance.load_markets()
    usdt_markets = [market.split("/")[0]  for market in markets.keys() if market.endswith("/USDT")]
    return templates.TemplateResponse("markets.html", {"request": request, "markets": usdt_markets})

@app.get("/markets/{symbol}")
async def market_symbol(symbol):
    symbol_info = get_symbol_info(symbol+"/USDT")
    return symbol_info

@app.post("/balance", response_class=HTMLResponse)
async def print_balance(request: Request):
    balance = str(get_balance())

    return HTMLResponse(balance)

@app.post("/cur_price", response_class=HTMLResponse)
async def print_cur_price(request: Request, symbol: str = Form(...)):
    cur_price = str(get_cur_price(symbol))
    return HTMLResponse(cur_price)

@app.post("/strategy", response_class=HTMLResponse)
async def select_strategy(request: Request, strategy: str = Form(...)):

    if strategy == "strategy_1":
        strategy_1()
        result = "전략 1"
    elif strategy == "strategy_2":
        result = "전략 2"
    elif strategy == "strategy_3":
        result = "전략 3"


    return templates.TemplateResponse(f"{file_name}.html", {"request": request, "result": result})



@app.post("/enter_position", response_class=HTMLResponse)
async def enter_position_endpoint(request: Request, symbol: str = Form(...), purchase_percent: float = Form(...), target: int = Form(...)):
    position = {
        "type":None,
        "amount":0
    }
    cur_price = get_cur_price(symbol)
    balance = get_balance()
    amount = calAmount(balance, cur_price, purchase_percent)
    enter_position(binance, symbol, cur_price, amount, target, position)
    return templates.TemplateResponse("position.html", {"request": request, "position": position})