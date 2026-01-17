from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..base import Base


class UserDepartment(Base):
    __tablename__ = "user_department"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    department_id = Column(Integer, nullable=False)
    position = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)

    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())
