from sqlalchemy import CheckConstraint, Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..base import Base


class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    category = Column(String(50), nullable=True)
    has_file = Column(Boolean, default=False)
    STATUS = ["pending", "approved", "rejected"]
    status = Column(String(20), default="pending")
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            f"status IN ({', '.join(repr(s) for s in STATUS)})",
            name="ck_application_status_valid",
        ),
    )
