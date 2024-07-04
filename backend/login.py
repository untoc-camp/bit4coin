from sqlalchemy import Column, Integer, String, DateTime

from db import Base


class Login(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    password = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)


