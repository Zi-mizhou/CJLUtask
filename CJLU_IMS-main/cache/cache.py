import redis.asyncio as redis
from typing import AsyncGenerator
from config.config import settings

# Redis 连接配置
REDIS_URL = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"  # 可以改为你的地址


async def get_redis_client() -> AsyncGenerator[redis.Redis, None]:
    client: redis.Redis = redis.from_url(REDIS_URL, decode_responses=True)

    try:
        yield client
    finally:
        await client.aclose()


def create_redis_client() -> redis.Redis:
    return redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0", decode_responses=True
    )
