import ccxt

apiKey = None
secret = None

binance = ccxt.binance(config={
    "apiKey": apiKey,
    "secret":secret,
    "enableRateLimit":True,
    "options":{"defaultType":"future"} # 선물거래 명시
})

