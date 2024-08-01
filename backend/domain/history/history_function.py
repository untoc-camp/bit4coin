from domain.history import history_crud, history_schema
from database import get_db
from fastapi import Depends, Query, HTTPException
from sqlalchemy.orm import Session
from strategys.env import profit_percent, loss_percent
from strategys.function import get_cur_price
from domain.user.user_router import get_current_user

from models import Item
import datetime

# history를 자동매매의 내역을 DB로 옮기는 작업
# strategys.stratefy.strategy_1, 2 , 3의 포지션에 진입하는 if문 안에 들어갈 예정
    

def create_history(symbol, position, entry_price, amount, cur_price, email):
    db = next(get_db())  # Depends 대신 직접 세션 객체 생성
    if position["type"] == "long":
        profit_end = entry_price + entry_price * profit_percent   
        loss_end = entry_price - entry_price * loss_percent
    elif position["type"] =="short":
        profit_end = entry_price - entry_price * profit_percent
        loss_end = entry_price + entry_price * profit_percent  

    # data 가공
    item_data = {
        "symbol": symbol,
        "position_type": position["type"],
        "enter_time": datetime.datetime.now().isoformat(),
        "close_time": datetime.datetime.now().isoformat(),
        "entry_price": entry_price,
        "cur_price": cur_price,
        "purchase_price": round(amount * entry_price, 4) , # amount * current_price 
        "eval_price": round(amount * cur_price, 4), # amount * current_price
        "eval_PAL": round(cur_price - entry_price, 4), # cur_price - entry_price
        "revenue_rate": round(((cur_price - entry_price)  / cur_price) * 100, 2)  , # round(((entry_price - current_price)  / current_price) * 100, 2) 
        "amount": amount,
        "profit_end": profit_end,
        "loss_end": loss_end,
        "owner_email": email # db에 들어가는 email : 현재 로그인된 current user의 email을 넣어야됨 
    }

    # db에 넣기 위해 우리가 정의한 schema 형식에 맞게 데이터 변환
    item_schema = history_schema.Item_schema(**item_data)

    # db에 데이터를 넣음
    created_item = history_crud.create_item(db, item_schema)   

    print(created_item)

# position 청산할 때 마지막 값을 바탕으로 DB에 업데이트
# strategys.stratefy.strategy_1, 2 , 3의 포지션을 청산하는 if문 안에 들어갈 예정
def update_history(cur_price):
    db = next(get_db())  # Directly creating a session object

    # Fetch the most recent item from the database
    item_data = db.query(Item).order_by(Item.id.desc()).first()
    if item_data:
        # Calculate new values
        eval_price = round(item_data.amount * cur_price, 4)
        eval_PAL = round(cur_price - item_data.entry_price, 4)
        revenue_rate = round(((cur_price - item_data.entry_price) / cur_price) * 100, 2)
        close_time = datetime.datetime.now()
        
        # data 변환 
        item_schema = history_schema.Item_schema(
            symbol=item_data.symbol,
            position_type=item_data.position_type,
            entry_price=item_data.entry_price,
            purchase_price=item_data.purchase_price,
            eval_price=eval_price, # 변동하는 값
            eval_PAL=eval_PAL, # 변동하는 값
            revenue_rate=revenue_rate, # 변동하는 값
            amount=item_data.amount,
            profit_end=item_data.profit_end,
            loss_end=item_data.loss_end,
            owner_email=item_data.owner_email,
            enter_time=item_data.enter_time,  
            close_time=close_time # 변동하는 값 : 종료 시간은 포지션이 종료된 시간으로 정의함
        )

        # 기존의 db table에 값을 update
        updated_item = history_crud.update_item_first(db, item_data.id, item_schema) 
        print(updated_item)

        return updated_item
    else:
        return None


# history 상단의 내용을 보여주는 함수 db 저장 x
# 변동하는 값들을 db에 저장하지 않고 호출만 함
def update_item(item, symbol, amount, entry_price): # -> 
    cur_price = get_cur_price(symbol)
    item.eval_price = round(amount * cur_price, 4)
    item.eval_PAL = round(cur_price - entry_price, 4)
    item.revenue_rate = round(((cur_price - entry_price)  / cur_price) * 100, 2) 
    item.close_time = datetime.datetime.now() 
    return item # -> history_router.history_list_first