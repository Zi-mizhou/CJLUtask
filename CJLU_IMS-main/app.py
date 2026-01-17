from contextlib import asynccontextmanager
from fastapi import FastAPI
from cache.cache import create_redis_client
from middleware.cookie_auth import CookieAuthMiddleware
from middleware.exception_handler import add_exception_handlers
from middleware.jwt_auth import JWTAuthMiddleware
from model.schema.schemas.base import BaseResponse
from router.v1.api import router
from config.config import settings

redis_client = create_redis_client()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router, prefix="/api/v1")

app.add_middleware(
    CookieAuthMiddleware,
    redis_client=redis_client,
    session_cookie_name="session_id",
    timestamp_cookie_name="timestamp",
)

app.add_middleware(JWTAuthMiddleware)

add_exception_handlers(app)


@app.get("/")
async def root():
    return BaseResponse.success(
        msg="Welcome to CJLU IMS API",
        data={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "description": settings.APP_DESCRIPTION,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
