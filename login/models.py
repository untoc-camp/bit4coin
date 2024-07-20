from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(Text, nullable=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    api_key = Column(Text, nullable=False)
    api_key_secret = Column(Text, nullable=False)