from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base

from datetime import datetime

# db table에 어떤 형식으로 데이터를 넣을지
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(Text, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    api_key = Column(Text, nullable=False)
    api_key_secret = Column(Text, nullable=False)


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False) # 코인
    position_type = Column(String, nullable=False)
    
    enter_time = Column(DateTime, nullable=False) # 진입 시각
    close_time = Column(DateTime, nullable=False) # 청산 시각

    entry_price = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    eval_price = Column(Float, nullable=False)
    eval_PAL = Column(Float, nullable=False)
    revenue_rate = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    
    profit_end = Column(Float, nullable=False)
    loss_end = Column(Float, nullable=False)

    onwer_id = Column(Integer, ForeignKey("users.id"))
    onwer = relationship("User", backref="item")
