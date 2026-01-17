from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..base import Base


class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=True)
    referer = Column(String(255), nullable=True)
    ip = Column(String(45), nullable=True)
    create_time = Column(DateTime, server_default=func.now())
