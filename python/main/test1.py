import time
from init import binance
from position import enter_position, exit_position
from function import get_cur_price, get_balance, dataFrame, calAmount, VolatilityBreakout 
from env import profit_percent, loss_percent, purchase_percent, con_diffma40_4, timeframe, symbols, k


##### 수수료 ####
# 지정가 : 0.02% * 2
# 시장가 : 0.04% * 2
################


# todo 
# 수익구조 계산해서 실제 수익률 파악하기 (0.8, 1.6 변경하기)
# 분할 매수기법 구현하기



def print_info(df):
    print("=================================ETH/USDT=============================================")
    print("----BASE----")
    print(f"sma4 : {sma4}, sma30 : {sma30}")
    print(f"long => {sma4 > sma30}       short => {sma4 < sma30}")
    print("----VB----")
    print(f"long_target : {long_target} /// cur_price  {cur_price}   => {long_target < cur_price}")
    print(f"short_target : {short_target} /// cur_price : {cur_price}   => {short_target > cur_price}")
    print("----position----")
    print(f"position : {position['type']}")
    print("----횡보조건----")
    print(f"횡보 조건 : {(diffma40_4 > con_diffma40_4)}")
    print(f"entry_price : {entry_price}")

    print("-----------------청산 조건-----------------")
    print(f"long profit end : {entry_price + entry_price * profit_percent} /// {cur_price}    => {entry_price + entry_price * profit_percent < cur_price}")
    print(f"long loss end : {entry_price - entry_price * loss_percent} /// {cur_price}    => {entry_price - entry_price * loss_percent > cur_price}")

    print(f"short profit end : {entry_price - entry_price * profit_percent} /// {cur_price}    => {entry_price - entry_price * profit_percent > cur_price}")
    print(f"short loss end : {entry_price + entry_price * loss_percent} /// {cur_price}    => {entry_price + entry_price * loss_percent < cur_price}")


entry_price = 0
position = {
    "type":None,
    "amount":0
}

while(1):
    # 현재가
    cur_price = get_cur_price(symbols[0])

    # 잔고
    balance = get_balance()

    # dataFrame 
    df = dataFrame(symbols[0])

    # 구매 수량
    amount = calAmount(balance, cur_price, purchase_percent) # 50% 

    # 변동성 돌파전략 
    long_target, short_target = VolatilityBreakout(dataFrame(symbols[0]))
    
    # sma 설정
    sma4 = df["sma4"].iloc[-1]
    sma8 = df["sma8"].iloc[-1]
    sma30 = df["sma30"].iloc[-1]
    sma40 = df["sma40"].iloc[-1]
    diffma40_4 = df["diffMa40_4"].iloc[-1]

    # long position 진입 조건
    is_long = ((sma4 > sma30) & (cur_price > long_target) & (diffma40_4 > con_diffma40_4) & (position["type"] == None)) 
    # short position 진입 조건
    is_short = ((sma4 < sma30) & (cur_price < short_target) & (diffma40_4 > con_diffma40_4) & (position["type"] == None)) 

    # long position 청산 조건
    is_long_end =  (((entry_price + entry_price * profit_percent < cur_price) and position["type"] == "long") or ((entry_price - entry_price * loss_percent > cur_price) and position["type"] == "long") )
    # short position 청산 조건
    is_short_end = (((entry_price - entry_price * profit_percent > cur_price) and position["type"] == "short") or ((entry_price + entry_price * loss_percent < cur_price) and position["type"] =="short"))
    # print(df)
    # position 진입
    if is_long:
        entry_price = cur_price
        print_info(df)
        enter_position(binance, symbol=symbols[0], cur_price = cur_price, amount=amount, target=1, position=position)

    if is_long_end:
        print_info(df)
        exit_position(binance, symbol=symbols[0], cur_price=cur_price, amount = position["amount"], position=position)
        
        
    if is_short:
        entry_price = cur_price
        print_info(df)
        enter_position(binance, symbol=symbols[0], cur_price = cur_price, amount=amount, target=-1, position=position)

    if is_short_end:
        print_info(df)
        exit_position(binance, symbol=symbols[0], cur_price=cur_price, amount = position["amount"], position=position)
        
    else:
        print_info(df)
    time.sleep(1)

