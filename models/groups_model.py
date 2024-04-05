from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class Groups(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    
    creator = Column(String(255))
    createdTime = Column(DateTime, default=func.now())
    modifier = Column(String(255))
    modifiedTime = Column(DateTime, default=func.now())
    is_activated = Column(Boolean, default=True)

    users = relationship("Users", back_populates="group")