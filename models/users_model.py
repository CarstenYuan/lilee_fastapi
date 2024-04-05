from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    group_id = Column(Integer, ForeignKey('groups.id'))

    creator = Column(String(255))
    createdTime = Column(DateTime, default=func.now())
    modifier = Column(String(255))
    modifiedTime = Column(DateTime, default=func.now())
    is_activated = Column(Boolean, default=True)

    group = relationship("Groups", back_populates="users")