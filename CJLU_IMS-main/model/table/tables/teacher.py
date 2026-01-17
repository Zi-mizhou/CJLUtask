from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, ForeignKey, Integer, String
from ..base import Base


class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    staff_no = Column(String(50), unique=True, nullable=False)
    title = Column(String(50), nullable=True)
    office_location = Column(String(100), nullable=True)

    def to_dict(self) -> dict:
        data = self.__dict__.copy()

        data.pop("_sa_instance_state", None)

        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()  # 转换为 ISO 8601 字符串
            elif isinstance(value, Decimal):
                data[key] = float(value)  # 或者 str(value) 以保留精度

        return data

    def to_str_dict(self) -> dict:
        data = self.__dict__.copy()

        for key, value in data.items():
            if not value:
                data[key] = ""
            if not isinstance(value, str):
                data[key] = str(value) or ""

        return data
