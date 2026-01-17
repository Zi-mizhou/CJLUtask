from sqlalchemy import Column, Integer, String, UniqueConstraint
from ..base import Base


class UserFile(Base):
    __tablename__ = "user_file"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    file_id = Column(Integer, nullable=False)
    permission = Column(String(20), nullable=False)  # e.g., 'read', 'write', 'delete'

    __table_args__ = (UniqueConstraint("user_id", "file_id", name="uq_user_file"),)
