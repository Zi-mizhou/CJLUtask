from datetime import datetime
from decimal import Decimal
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.sql import func
from ..base import Base
import bcrypt


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ROLE = ["admin", "teacher", "chairman", "director", "minister", "member", "student"]
    role = Column(String(10), nullable=False, index=True)

    username = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)  # 应该是哈希值

    name = Column(String(100), nullable=True)

    gender = Column(String(10), nullable=True)

    avatar_url = Column(String(255), nullable=True)

    email = Column(String(100), unique=True, nullable=True)
    is_active = Column(Boolean, default=True)

    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def verify_password(self, password: str) -> bool:
        pwd_bytes = password.encode("utf-8")
        hash_bytes = self.password.encode("utf-8")
        return bcrypt.checkpw(pwd_bytes, hash_bytes)

    def to_dict(self) -> dict:
        data = self.__dict__.copy()

        data.pop("_sa_instance_state", None)
        data.pop("password", None)
        data.pop("create_time", None)
        data.pop("update_time", None)

        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()  # 转换为 ISO 8601 字符串
            elif isinstance(value, Decimal):
                data[key] = float(value)  # 或者 str(value) 以保留精度

        return data

    def to_str_dict(self) -> dict:
        data = self.__dict__.copy()

        data.pop("_sa_instance_state", None)
        data.pop("password", None)
        data.pop("create_time", None)
        data.pop("update_time", None)

        for key, value in data.items():
            if not isinstance(value, str):
                data[key] = str(value) or ""

        return data

    @staticmethod
    def hash_password(password: str) -> str:
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(pwd_bytes, salt)
        return hashed.decode("utf-8")  # 占位符

    @staticmethod
    def filter_info(data: dict) -> dict:
        not_allowed_keys = {
            "password",
            "create_time",
            "update_time",
            "id",
            "user_id",
        }
        return {
            key: value for key, value in data.items() if key not in not_allowed_keys
        }
