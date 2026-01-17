import re
from sqlalchemy import CheckConstraint, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..base import Base


class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 1/1/1 类似路径
    path = Column(String(255), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    parent_id = Column(
        Integer,
        nullable=True,
        index=True,
    )
    description = Column(String(255), nullable=True)

    is_active = Column(Integer, default=1)  # 1表示激活，0表示禁用

    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # 数据库层面：确保 path 格式合法（PostgreSQL 示例）
    __table_args__ = (
        CheckConstraint(
            "path ~ '^[0-9]+(/[0-9]+)*$'", name="ck_department_path_format"
        ),
    )

    def __init__(
        self, path: str, name: str, parent_id: int = None, description: str = None
    ):
        # 应用层校验（兼容所有数据库）
        if not self._is_valid_path(path):
            raise ValueError(
                f"Invalid department path format: '{path}'. Expected format: '1', '1/2', '1/2/3', etc."
            )
        super().__init__(
            path=path, name=name, parent_id=parent_id, description=description
        )

    @staticmethod
    def _is_valid_path(path: str) -> bool:
        """
        校验 path 是否符合格式：仅由数字和 '/' 组成，
        不以 '/' 开头或结尾，且不包含连续 '/'
        """
        if not path or path.startswith("/") or path.endswith("/"):
            return False
        if "//" in path:
            return False
        return bool(re.match(r"^[0-9]+(/[0-9]+)*$", path))

    def get_level(self) -> int:
        """返回当前部门的层级深度（根为 0）"""
        return self.path.count("/")

    def is_ancestor_of(self, other) -> bool:
        """判断当前部门是否是 other 的祖先"""
        return other.path.startswith(self.path + "/")

    def is_descendant_of(self, other) -> bool:
        """判断当前部门是否是 other 的后代"""
        return self.path.startswith(other.path + "/")

    def __repr__(self):
        return f"<Department(id={self.id}, path='{self.path}', name='{self.name}')>"
