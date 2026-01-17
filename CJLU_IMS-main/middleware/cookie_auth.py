# middleware/cookie_auth.py
import re
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import redis.asyncio as redis

from model.schema.schemas.base import BaseResponse


class CookieAuthMiddleware(BaseHTTPMiddleware):
    # 公开路径（无需 cookie）
    PUBLIC_PATHS = [
        "/",
        "/api/v1/auth/public-key",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/docs",
        "/openapi.json",
        "/favicon.ico",
    ]
    # 支持正则（可选）
    PUBLIC_PATTERNS = []

    def __init__(
        self,
        app,
        redis_client: redis.Redis,
        session_cookie_name: str = "session_id",
        timestamp_cookie_name: str = "timestamp",
    ):
        super().__init__(app)
        self.redis = redis_client
        self.session_cookie_name = session_cookie_name
        self.timestamp_cookie_name = timestamp_cookie_name

    def _is_public_path(self, path: str) -> bool:
        """判断是否为公开路径"""
        if path in self.PUBLIC_PATHS:
            return True
        for pattern in self.PUBLIC_PATTERNS:
            if re.match(pattern, path):
                return True
        return False

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # 跳过公开路径
        if self._is_public_path(path):
            return await call_next(request)

        # 1. 获取 Cookie
        session_id = request.cookies.get(self.session_cookie_name)
        timestamp = request.cookies.get(self.timestamp_cookie_name)

        if not session_id or not timestamp:
            return JSONResponse(
                status_code=200,
                content=BaseResponse.fail(
                    code=401, msg="认证失败,缺少会话信息"
                ).model_dump(),
            )

        # 2. 构造 Redis key
        redis_key = f"session:{timestamp}"

        # 3. 从 Redis 查询
        stored_session_id = await self.redis.get(redis_key)

        # 4. 验证
        if not stored_session_id:
            return JSONResponse(
                status_code=200,
                content=BaseResponse.fail(
                    code=401, msg="认证失败,会话已过期"
                ).model_dump(),
            )

        if stored_session_id != session_id:
            return JSONResponse(
                status_code=200,
                content=BaseResponse.fail(
                    code=401, msg="认证失败,会话无效"
                ).model_dump(),
            )

        # ✅ 验证通过，继续
        return await call_next(request)
