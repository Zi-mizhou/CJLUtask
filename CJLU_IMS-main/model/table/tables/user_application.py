from sqlalchemy import Column, DateTime, Integer, UniqueConstraint, func
from ..base import Base


class UserApplication(Base):
    __tablename__ = "user_application"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, nullable=False)
    receive_id = Column(Integer, nullable=False)
    application_id = Column(Integer, nullable=False)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint(
            "sender_id", "receive_id", "application_id", name="uq_user_app"
        ),
    )
