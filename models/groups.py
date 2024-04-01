from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    users = relationship("Users", back_populates="group")