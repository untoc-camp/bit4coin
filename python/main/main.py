from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import ccxt
import math
import pandas as pd
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

with open("../apiKey.txt") as f:
    lines = f.readlines()
    apiKey = lines[0].strip()
    secret = lines[1].strip()

binance = ccxt.binance(config={
    "apiKey": apiKey,
    "secret": secret,   
    "enableRateLimit": True,
    "options": {"defaultType": "future"}  # 선물거래 명시
})

########## 코인의 현재가 가져오기 ##########
def getcurrentPrice(coinName):
    coin = binance.fetch_ticker(coinName)
    print("현재가 :", coin["last"])
    return coin["last"]

# 코인 구매 수량 계산
def calAmount(balance, cur_price, purchase_percent=0.1):
    Trade = balance * purchase_percent  # 전체 자본의 portion : 10%
    MTA = 100000  # Minimum Trade Amount : 해당 숫자는 코인마다 상이하므로 수정해야함 0.00001
    amount = math.floor((Trade * MTA) / cur_price) / MTA
    return amount

def get_balance(): 
    # 잔고 조회
    balance = binance.fetch_balance()
    # USDT 잔고 조회
    USDTBalance = balance["total"]["USDT"]
    return USDTBalance

########## 코인 정보 출력 ##########
def getCoin(coinName):
    coin = binance.fetch_ticker(coinName)
    return coin

def dataFrame(symbol):
    # 데이터프레임 객체로 변환
    btcOHLCV = binance.fetch_ohlcv(symbol, timeframe="15m", limit=5000)
    df = pd.DataFrame(btcOHLCV, 
                    columns=["datetime", "open", "high", "low", "close", "volume"])
    df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")  + pd.Timedelta(hours=9)

    df.set_index("datetime", inplace=True)

    # sma 설정 : ema는 trading view의 계산값이랑 오차가 있음
    df["sma4"] = df["close"].rolling(4).mean()
    df["sma8"] = df["close"].rolling(8).mean()
    df["sma30"] = df["close"].rolling(30).mean()
    df["sma40"] = df["close"].rolling(40).mean()

    df["diffMa40_4"] = abs(df["sma40"] - df["sma4"])
    
    return df

def enter_position(exchange, symbol, cur_price, amount, target, position):
    if target == 1:
        position["type"] = "long"
        position["amount"] = amount
        # exchange.create_market_buy_order(symbol=symbol, amount=amount)
        print(":::::::enter long")
    elif target == -1:
        position["type"] = "short"
        position["amount"] = amount
        # exchange.create_market_sell_order(symbol=symbol, amount=amount)
        print(":::::::enter short")
    else:
        print(":::::::매수 X")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/{id}")
def test(id: int):
    return {"message": id}

@app.post("/strategy", response_class=HTMLResponse)
async def execute_strategy(request: Request, strategy: str = Form(...), coinName: str = Form(...)):
    if strategy == "balance":
        result = get_balance()
    elif strategy == "cur_price":
        result = getcurrentPrice(coinName)
    
    coin_data = dataFrame(coinName)["sma4"]
    print(coin_data)

    print(f"Result: {result}")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "getCoin": coin_data,
        "result": result,
        "strategy": strategy,
        "coinName": coinName
    })

@app.post("/enter_position", response_class=HTMLResponse)
async def enter_position_endpoint(request: Request, symbol: str = Form(...), cur_price: float = Form(...), amount: float = Form(...), target: int = Form(...)):
    position = {}
    enter_position(binance, symbol, cur_price, amount, target, position)
    
    return templates.TemplateResponse("index.html", {"request": request, "position": position})
