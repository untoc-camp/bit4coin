# from models import User, Item
# from datetime import datetime
# from database import SessionLocal

# user_data = User(user_name="hife",
#                  email="123@123" ,
#                  password="1234", 
#                  create_date=datetime.utcnow(), 
#                  api_key="123456789", 
#                  api_key_secret="qwer"
#                  )

    
# # Item_data = Item(symbol = "ETH/USDT", 
# #                  position_type =1,
# #                  enter_time = datetime.now(),
# #                  close_time = datetime.now(),
# #                  entry_price = 3771.1,
# #                  purchase_price = 0.5,
# #                  eval_price = 450.2,
# #                  eval_PAL = -1.7,
# #                  revenue_rate = 2.3,
# #                  amount=0.00123,
# #                  profit_end = 33901.2,
# #                  loss_end=2627.9121,
# #                  onwer_id=1
# #                  )

# db = SessionLocal()
# db.add(user_data)
# db.commit()