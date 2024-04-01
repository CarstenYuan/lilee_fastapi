from sqlalchemy import Column, Integer, String
from .base import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    group_id = Column(Integer)
