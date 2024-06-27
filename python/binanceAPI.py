import ccxt
import pprint
import time
import pandas as pd

with open("apiKey.txt") as f:
    lines = f.readlines()
    apiKey = lines[0].strip()
    secret = lines[1].strip()

binance = ccxt.binance(config={
    "apiKey": apiKey,
    "secret":secret,
    "enableRateLimit":True,
    "options":{"defaultType":"future"} # 선물거래 명시 : api발급 및 wifi 연결
})

symbol = "ETH/USDT"


def get_markets_info():
    # 선물 마켓 조회
    markets = binance.load_markets()
    for m in markets:
        if m.endswith("/USDT"):
            print(m)    
    return markets


def get_curPrice(symbol):
    while(1):
        # 현재가 조회
        coin = binance.fetch_ticker(symbol)
        cur_price = coin["last"]
        print("현재가 : {:.4f}".format(cur_price))
        time.sleep(1)

def get_OHLCV(symbol):
    # 선물 OHLCV 조회
    coinOHLCV = binance.fetch_ohlcv(symbol=symbol, timeframe="15m", since=None, limit=1000)

    df = pd.DataFrame(coinOHLCV, columns=["datetime", "open", "high","low","clsoe","volume"])
    df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")
    df.set_index("datetime", inplace=True)
    print(df)


def get_balance():
    # 선물 잔고 조회
    balance = binance.fetch_balance()
    print(balance["total"])

def set_leverage(symbol):
    # leverage 설정
    markets = binance.load_markets()
    market = binance.market(symbol)
    leverage = 3
    resp = binance.fapiprivate_post_leverage({
        "symbol":market["id"], 
        "leverage":leverage
    })
    print(resp)


# get_markets_info()
# get_curPrice(symbol)
# get_OHLCV(symbol)
# get_balance()
# set_leverage(symbol)

# binance.create_market_buy_order(symbol=symbol, amount=0.01)
# binance.create_market_sell_order(symbol=symbol, amount=0.01)

