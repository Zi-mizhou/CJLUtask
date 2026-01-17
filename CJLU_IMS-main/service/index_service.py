from fastapi import Depends
import redis.asyncio as redis

from cache.cache import get_redis_client
from common.constants import TABS
import json


class IndexService:

    def __init__(self, cache: redis.Redis):
        self.cache = cache

    # ["admin", "teacher", "chairman", "director", "minister", "member", "student"]
    async def get_tabs(self, role: str) -> dict:
        tabs = await self.cache.get(f"tabs:{role}")
        if tabs:
            json_tabs = json.loads(tabs)
            return {"tabs": json_tabs}

        if role == "admin":
            not_allowed_tab_names = []
        elif role == "teacher":
            not_allowed_tab_names = ["Admin"]
        elif role == "chairman":
            not_allowed_tab_names = ["Admin"]
        elif role == "director":
            not_allowed_tab_names = ["Admin"]
        elif role == "minister":
            not_allowed_tab_names = ["Admin"]
        elif role == "member":
            not_allowed_tab_names = ["Admin", "Management", "Application"]
        else:
            return {"tabs": []}
        tabs = self.filter_tabs(TABS, not_allowed_tab_names)
        pipe = self.cache.pipeline()
        pipe.setex(f"tabs:{role}", 60 * 30, json.dumps(tabs))
        await pipe.execute()

        return {"tabs": tabs}

    def filter_tabs(
        self, tabs: list[dict], not_allowed_tab_names: list[str]
    ) -> list[dict]:
        return [
            tab for tab in tabs if tab["name"] not in (not_allowed_tab_names + ["Home"])
        ]


def get_index_service(
    cache: redis.Redis = Depends(get_redis_client),
) -> IndexService:
    return IndexService(cache)
