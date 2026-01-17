# middleware/jwt_middleware.py
import re
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from typing import Callable
from config.config import settings
from model.schema.schemas.base import BaseResponse


class JWTAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exempt_paths=None):
        super().__init__(app)
        self.PUBLIC_PATHS = exempt_paths or [
            "/",
            "/assets/",
            "/api/v1/auth/public-key",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/admin",
            "/docs",
            "/openapi.json",
            "/favicon.ico",
        ]
        self.PUBLIC_PATTERNS = []
        self.bearer = HTTPBearer(auto_error=False)  # 我们手动处理错误

    def _is_public_path(self, path: str) -> bool:
        """判断是否为公开路径"""
        if path in self.PUBLIC_PATHS:
            return True
        for pattern in self.PUBLIC_PATTERNS:
            if re.match(pattern, path):
                return True
        return False

    async def dispatch(self, request: Request, call_next: Callable):
        path = request.url.path

        # 白名单路径直接放行
        if self._is_public_path(path):
            response = await call_next(request)
            return response

        # 提取 Authorization 头
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=200,
                content=BaseResponse.fail(
                    code=401, msg="认证失败,缺少令牌"
                ).model_dump(),
            )

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                return JSONResponse(
                    status_code=200,
                    content=BaseResponse.fail(
                        code=401, msg="认证失败,令牌无效"
                    ).model_dump(),
                )
        except ValueError:
            return JSONResponse(
                status_code=200,
                content=BaseResponse.fail(
                    code=401, msg="认证失败,令牌无效"
                ).model_dump(),
            )

        # 验证 JWT
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
            request.state.user_id = payload.get("id")
            request.state.role = payload.get("role")
            request.state.jwt_payload = payload
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=200,
                content=BaseResponse.fail(
                    code=401, msg="认证失败,令牌已过期"
                ).model_dump(),
            )
        except jwt.InvalidTokenError as e:
            return JSONResponse(
                status_code=200,
                content=BaseResponse.fail(
                    code=401, msg="认证失败,令牌无效"
                ).model_dump(),
            )
        # 继续处理请求
        response = await call_next(request)
        return response
