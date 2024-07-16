from models import Item
from sqlalchemy.orm import Session


from domain.history import history_schema
import datetime

# 가장 최근에 진입한 포지션의 정보를 불러옴 
def get_item_list_first(db: Session):
    item_list_first= db.query(Item).order_by(Item.enter_time.desc()).first()
    print(item_list_first)
    return [item_list_first] # 리스트 형태


# 가장 최근에 진입한 포지션을 제외한 정보를 불러옴
def get_item_list(db: Session):
    item_list = db.query(Item).order_by(Item.enter_time.desc()).offset(1).all()
    print(item_list)
    return item_list



# db에 데이터를 넣는 과정
def create_item(db: Session, item_schema: history_schema.Item_schema): # item_schema의 타입을 올바르게 지정합니다.
    Item_data = Item(symbol=item_schema.symbol, 
                     position_type=item_schema.position_type,
                     enter_time=datetime.datetime.now(),
                     close_time=datetime.datetime.now(),
                     entry_price=item_schema.entry_price,
                     purchase_price=item_schema.purchase_price,
                     eval_price=item_schema.eval_price,
                     eval_PAL=item_schema.eval_PAL,
                     revenue_rate=item_schema.revenue_rate,
                     amount=item_schema.amount,
                     profit_end=item_schema.profit_end,
                     loss_end=item_schema.loss_end,
                     onwer_id=item_schema.onwer_id)

    db.add(Item_data)
    db.commit()
    db.refresh(Item_data)

    return Item_data # -> history_function.create_history

# 가장 상단의 데이터를 포지션 종료할 때 db에 저장
def update_item_first(db: Session, item_id: int, item_schema: history_schema.Item_schema): 
    # 가장 상단의 데이터
    item_data = db.query(Item).filter(Item.id == item_id).first()

    # 변동하는 데이터만 가져옴 : 다른 데이터는 변환 없음
    if item_data:
        item_data.eval_price = item_schema.eval_price
        item_data.eval_PAL = item_schema.eval_PAL
        item_data.revenue_rate = item_schema.revenue_rate

        db.commit()
        db.refresh(item_data)

        return item_data
    else:
        return None

