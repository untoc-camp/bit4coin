from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from strategys.init import binance
from strategys.position import enter_position, exit_position
from strategys.function import get_cur_price, get_balance, dataFrame, calAmount, VolatilityBreakout, get_symbol_info, dataFrame_day
from strategys.env import profit_percent, loss_percent, purchase_percent, con_diffma40_4, timeframe, symbols, k
from strategys.strategy import strategy_1, strategy_2, strategy_3


from pydantic import BaseModel
from typing import Dict
import datetime
import concurrent.futures

from domain.history import history_router
app = FastAPI()


# Add CORS middleware
origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Enter_info(BaseModel):
    strategy : str
    symbol : str
    purchase_percent : float
    leverage : int
    # create_date: datetime.datetime


@app.get("/")
async def init(request: Request):
    return {"message":"home"}


def position(strategys, symbol, purchase_percent, leverage):
    if strategys == "strategy_1":
        strategy_1(symbol, purchase_percent, leverage)
    elif strategys == "strategy_2":
        strategy_2(symbol, purchase_percent, leverage)
    elif strategys == "strategy_3":
        strategy_3(symbol, purchase_percent, leverage)

# 실제로 포지션에 진입하기 위한 post
@app.post("/enter_position", response_model=Enter_info)
async def enter_position(enter_info: Enter_info, background_tasks:BackgroundTasks): # enter_info의 양식대로 데이터가 들어옴
    background_tasks.add_task(position, 
                              enter_info.strategy, 
                              enter_info.symbol, 
                              enter_info.purchase_percent, 
                              enter_info.leverage)
    return enter_info

# symbols_info를 return 함
@app.get("/symbols_info", response_class=JSONResponse)
async def symbols_info():
    symbols = ["ETH/USDT", "BTC/USDT", "XRP/USDT", "DOGE/USDT", "SOL/USDT", "STX/USDT"]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 병렬로 dataFrame_day 함수를 호출합니다.
        dataframes = list(executor.map(dataFrame_day, symbols))

    data = {}
    for symbol, df in zip(symbols, dataframes):
        cur_price, daily_per = get_symbol_info(symbol, df)
        data[f"{symbol.split('/')[0]}_cur_price"] = cur_price
        data[f"{symbol.split('/')[0]}_daily_per"] = daily_per

    return JSONResponse(content=data)

# @app.get("/history", response_class=HTMLResponse)
# def history(request: Request):
#     return templates.TemplateResponse("history.html", {"request": request})

# @app.get("/mypage", response_class=HTMLResponse)
# def mypage(request: Request):
#     return templates.TemplateResponse("mypage.html", {"request": request})

# @app.get("/setting", response_class=HTMLResponse)
# def mypage(request: Request):
#     return templates.TemplateResponse("setting.html", {"request": request})




app.include_router(history_router.router)