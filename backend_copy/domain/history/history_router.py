from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from domain.history import history_schema, history_crud
from models import Item

from domain.history.history_function import update_item
router = APIRouter(
    prefix="/history",
)


# 1. history의 main_top은 1초마다 데이터를 들고올 예정 : 
# 평가손익, 평가금액, 수익률을 실시간으로 업데이트 할 것(이건 DB에 실시간으로 저장 X) - > 청산할 때 DB에 저장 
# -> 청산이후 list에서 반영된 값을 보여줌

# 2. 포지션을 청산할 때 평가손익, 평가금액, 수익률 등의 변동된 값을 업데이트하고 반영해줌


# history의 가장 최근의 item을 보여줌
@router.get("/list_first", response_model=List[history_schema.Item_schema])
def history_list_first(db: Session = Depends(get_db)):
    _history_list_first = history_crud.get_item_list_first(db)

    # current_price가 필요한 변수들은 DB의 내용을 조금 변화 시켜서 보여줌
    item = _history_list_first[0]
    print(item)
    _history_list_first = update_item(item, item.symbol, item.amount, item.entry_price)

    return [_history_list_first] # 리스트형태로 반환 - > history.js에서 fetch함

# 가장 최근의 item을 제외한 history의 목록을 보여줌
@router.get("/list", response_model=List[history_schema.Item_schema])
def history_list(db: Session = Depends(get_db)):
    _history_list = history_crud.get_item_list(db) # 상단의 item을 제외한 데이터를 불러옴

    return _history_list

# data를 넣는건데 실제로 사용은 안함
@router.post("/create_item", response_model=history_schema.Item_schema)
def create_item(item_schema: history_schema.Item_schema, db: Session = Depends(get_db)):
    _create_item = history_crud.create_item(db, item_schema)
    if _create_item is None:
        raise HTTPException(status_code=400, detail="Failed to create item")
    return _create_item
