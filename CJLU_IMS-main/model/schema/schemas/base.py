# schemas/common.py
from pydantic import BaseModel
from typing import TypeVar, Optional, Dict, Any

T = TypeVar("T")


class BaseResponse(BaseModel):
    """
    统一响应结构
    {
        "code": 200,
        "msg": "OK",
        "data": { ... }
    }
    """

    code: int
    msg: str
    data: Optional[Any] = None

    @classmethod
    def success(cls, data=None, msg="Success"):
        return cls(code=200, msg=msg, data=data)

    @classmethod
    def fail(cls, code=400, msg="Failed"):
        return cls(code=code, msg=msg, data=None)
