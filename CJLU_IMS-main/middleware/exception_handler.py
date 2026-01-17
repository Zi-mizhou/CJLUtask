# middleware/exception_handler.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from model.exception.base_exceptions import CustomException
from utils.logger import logger


async def custom_exception_handler(request: Request, exc: CustomException):
    user_id = getattr(request.state, "user_id", None)
    logger.warning(
        f"ip:{request.client.host},{f'用户:{user_id},' if user_id is not None else ''}访问:{request.url},发生异常:{exc.message}"
    )
    return JSONResponse(
        status_code=200,
        content={"code": exc.status_code, "msg": exc.message, "data": None},
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    user_id = getattr(request.state, "user_id", None)
    logger.warning(
        f"ip:{request.client.host},{f'用户:{user_id},' if user_id is not None else ''}访问:{request.url},发生异常:{exc.detail}"
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "msg": exc.detail, "data": None},
    )


async def general_exception_handler(request: Request, exc: Exception):
    user_id = getattr(request.state, "user_id", None)
    logger.error(
        f"ip:{request.client.host},{f'用户:{user_id},' if user_id is not None else ''}访问:{request.url},发生异常:{exc.detail if isinstance(exc, HTTPException) else str(exc)}"
    )
    # 非自定义异常，默认 500
    return JSONResponse(
        status_code=500,
        content={"code": 500, "msg": "Server error", "data": None},
    )


def add_exception_handlers(app):
    """注册所有异常处理器"""
    app.add_exception_handler(CustomException, custom_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
