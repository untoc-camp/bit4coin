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

# 포지션 종료
def exit_position(exchange, symbol, cur_price, amount, position):
    if position["type"] =="long":
        # exchange.create_market_sell_order(symbol=symbol, amount=amount)
        print(":::::::exit long")
        position["type"] = None
    elif position["type"] == "short":
        # exchange.create_market_buy_order(symbol=symbol, amount=amount)
        print(":::::::exit short")
        position["type"] = None
