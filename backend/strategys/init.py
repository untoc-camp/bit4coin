import ccxt

# with open("../apiKey.txt") as f:
#     lines = f.readlines()
apiKey = 'vWUSh3fhD3TDE0i4AFN5dB4L8zoabvcebPYPfO5bGksjTYPcXUICO4zXiyWQfRbT'#lines[0].strip()
secret = '2M9wXgwJirREyOkxW4ZjwWC4q1EZxZ6Rv0JZlJduPQCqlJe8Z4iuSsu5sab25Iib'#lines[1].strip() apikey db에서 받아오는건 db 연동하고 하겠습니다.

binance = ccxt.binance(config={
    "apiKey": apiKey,
    "secret":secret,
    "enableRateLimit":True,
    "options":{"defaultType":"future"} # 선물거래 명시
})

