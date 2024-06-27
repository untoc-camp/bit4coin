import matplotlib.pyplot as plt
import pandas as pd
import ccxt


# 수익률, 승률, 코인 그래프

with open("apiKey.txt") as f:
    lines = f.readlines()
    apiKey = lines[0].strip()
    secret = lines[1].strip()

binance = ccxt.binance(config={
    "apiKey": apiKey,
    "secret":secret,
    "enableRateLimit":True,
    "options":{"defaultType":"future"} # 선물거래 명시
})

# 데이터 불러오기
df_ETH = pd.read_csv("ETH_0408-0508.csv", encoding='cp949')
df_BTC = pd.read_csv("BTC_0408-0508.csv", encoding='cp949')


symbol = "ETH/USDT"
df_symbol = df_ETH


# O,H,L,C,V 조회
def dataFrame(symbol):
    # 데이터프레임 객체로 변환
    COIN_OHLCV = binance.fetch_ohlcv(symbol, timeframe="15m", limit=1200)
    df = pd.DataFrame(COIN_OHLCV, 
                    columns = ["datetime", "open", "high", "low", "close", "volume"])
    coin_data = df.iloc[:, 4]
    c_data =[]
    print(coin_data)
    for i in range(1200):
        c_data.append(coin_data[i])
    return c_data

def get_data(df):
    # 수익 데이터 추출
    profit_data = df.iloc[:, 4]
    winning_data = df.iloc[:, 5]
    p_data = []
    w_data = []
    print(profit_data)
    for i in range(31):
        if profit_data[i] != "-":
            p_data.append(float(profit_data[i]))
            w_data.append(float(winning_data[i]))

    return df, p_data, w_data

def plot(symbol):
    # 그래프 그리기
    plt.subplot(311)
    plt.plot(range(len(p_data)), p_data, marker="o")
    plt.xlabel("Index")
    plt.ylabel("profit")
    plt.title(f"{symbol} - profit")
    plt.xticks(rotation=45)  # x축 라벨 회전
    plt.grid(True)
    
    plt.subplot(312)
    plt.plot(range(len(w_data)), w_data, marker="o", color="red")
    plt.xlabel("Index")
    plt.ylabel("winning rate")
    plt.title(f"{symbol} - winning rate")
    plt.xticks(rotation=45)  # x축 라벨 회전
    plt.grid(True)

    plt.subplot(313)
    plt.plot(range(len(c_data)), c_data, color="green")
    plt.xlabel("Index")
    plt.ylabel("Price")
    plt.title(f"{symbol} - coin data")
    plt.xticks(rotation=45)  # x축 라벨 회전
    plt.grid(True)

    plt.show()


df, p_data, w_data = get_data(df_symbol)
c_data = dataFrame(symbol)
plot(symbol)
