from .init import binance
from .env import k, timeframe
import pandas as pd
import math
import ccxt
# O,H,L,C,V 조회
def dataFrame(symbol):
    # 데이터프레임 객체로 변환
    OHLCV = binance.fetch_ohlcv(symbol, timeframe=timeframe, limit=5000)
    df = pd.DataFrame(OHLCV, 
                    columns = ["datetime", "open", "high", "low", "close", "volume"])
    df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")  + pd.Timedelta(hours=9)

    df.set_index("datetime", inplace=True)

    # sma 설정 : ema는 trading view의 계산값이랑 오차가 있음
    df["sma4"] = df["close"].rolling(10).mean()
    df["sma8"] = df["close"].rolling(30).mean()
    df["sma30"] = df["close"].rolling(80).mean()
    df["sma40"] = df["close"].rolling(120).mean()

    df["diffMa40_4"] = abs(df["sma40"] - df["sma4"])

    return df

def dataFrame_day(symbol):
    try:
        # 데이터프레임 객체로 변환
        OHLCV = binance.fetch_ohlcv(symbol, timeframe="1d", limit=5000)
        df = pd.DataFrame(OHLCV, 
                        columns = ["datetime", "open", "high", "low", "close", "volume"])
        df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")  + pd.Timedelta(hours=9)
        return df
    except ccxt.BaseError as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return pd.DataFrame()
    
# 코인 구매 수량 계산
def calAmount(balance, cur_price, purchase_percent = 0.1):
    Trade = balance * purchase_percent # 전체 자본의 portion : 10%
    MTA = 100000 # Minimum Trade Amount : 해당 숫자는 코인마다 상이하므로 수정해야함 0.00001
    amount = math.floor((Trade * MTA)/cur_price) / MTA 
    return amount

# 잔고 조회
def get_balance(): 
    # 잔고 조회
    balance = binance.fetch_balance()
    # USDT 잔고 조회
    USDTBalance = balance["total"]["USDT"]
    return USDTBalance

# 현재가 조회
def get_cur_price(symbol):
    # 현재가
    coin = binance.fetch_ticker(symbol)
    cur_price = coin["last"]
    return cur_price

#############################################################

# 변동성 돌판전략
def VolatilityBreakout(df):
    preCandle = df.iloc[-2]
    curcandle = df.iloc[-1]
    preCandleHigh = preCandle["high"] # 전 봉의 고가
    preCandleLow = preCandle["low"] # 전 봉의 저가
    curCandleOpen = curcandle["open"] # 현재 봉의 시가
    target = (preCandleHigh - preCandleLow) * k # 고가 - 저가
    longTarget = curCandleOpen + target # 롱 타겟
    shortTarget = curCandleOpen - target # 숏 타겟
    return longTarget, shortTarget


def get_symbol_info(symbol, df):
    cur_price = get_cur_price(symbol)
    daily_percent = round(((cur_price - df.iloc[-1]["open"])  / df.iloc[-1]["open"]) * 100, 2)    # 9시를 시작가격으로 봄
    return cur_price, daily_percent

