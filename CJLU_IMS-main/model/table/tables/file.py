from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..base import Base
from datetime import datetime


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    size = Column(Integer, nullable=True)  # size in bytes
    url = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)  # e.g., 'pdf', 'docx'
    parent = Column(Integer, nullable=True)
    is_dir = Column(Integer, default=0)  # 1 for directory, 0 for file
    active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    public = Column(Integer, default=0)  # 1 for public, 0 for private
    key = Column(String(255), nullable=True)  # OSS storage key
    create_time = Column(DateTime, server_default=func.now(), default=datetime.now())
    update_time = Column(
        DateTime, server_default=func.now(), default=datetime.now(), onupdate=func.now()
    )

    def to_dict(self) -> dict:
        data = self.__dict__.copy()
        data.pop("_sa_instance_state", None)
        data.pop("url", None)  # Remove URL for privacy
        data.pop("key", None)  # Remove key for privacy
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat()
        return data
