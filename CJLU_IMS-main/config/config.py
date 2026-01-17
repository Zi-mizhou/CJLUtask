# config/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    FRONTEND_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    REDIS_HOST: str
    REDIS_PORT: int
    LOCALHOST_REDIS_PATH: str
    ENVIRONMENT: str = "development"  # 默认为开发环境

    APP_NAME: str
    APP_VERSION: str
    APP_DESCRIPTION: str

    OSS_ENDPOINT_URL: str
    OSS_REGION_NAME: str
    OSS_ACCESS_KEY_ID: str
    OSS_ACCESS_KEY_SECRET: str
    OSS_BUCKET_NAME: str
    OSS_EXPIRE_URL_SECONDS: int

    JWT_AUTH_EXEMPT_PATHS: List[str] = [
        "/",
        "/assets/",
        "/auth/login",
        "/auth/register",
        "/project/update_order",
        "/admin",
        "/docs",
        "/openapi.json",
    ]
    COOKIE_AUTH_EXEMPT_PATHS: List[str] = [
        "/",
        "/index/login",
        "/api/public-key",
        "/docs",
        "/openapi.json",
        "/favicon.ico",
    ]

    # 使用新的 model_config
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, arbitrary_types_allowed=True
    )


# 实例化
settings = Settings()
