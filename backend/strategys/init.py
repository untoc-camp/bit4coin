import ccxt

# with open("../apiKey.txt") as f:
#     lines = f.readlines()
apiKey = None#lines[0].strip()
secret = None#lines[1].strip()

binance = ccxt.binance(config={
    "apiKey": apiKey,
    "secret":secret,
    "enableRateLimit":True,
    "options":{"defaultType":"future"} # 선물거래 명시
})

