import datetime

from pydantic import BaseModel


# 입력 양식

class Item_schema(BaseModel):
    symbol: str
    position_type: str
    
    enter_time : datetime.datetime # 진입 시각
    close_time : datetime.datetime # 청산 시각

    entry_price : float
    purchase_price : float
    eval_price : float
    eval_PAL : float
    revenue_rate : float
    amount : float
    
    profit_end : float
    loss_end : float

    onwer_id : int


    class Config:
        from_attributes = True