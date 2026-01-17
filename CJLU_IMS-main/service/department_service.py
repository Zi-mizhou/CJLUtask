import json
import time
import uuid
from fastapi import Depends
from cache.cache import get_redis_client
from mapper.department_mapper import DepartmentMapper
import redis.asyncio as redis
import base64
from mapper.user_department_mapper import UserDepartmentMapper
from model.schema.schemas.department import (
    CreateDepartmentRequest,
    UpdateDepartmentRequest,
)
from utils.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession


class DepartmentService:
    def __init__(self, cache: redis.Redis):
        self.cache = cache
        self.department_mapper = DepartmentMapper()
        self.user_department_mapper = UserDepartmentMapper()

    async def get_department_details(
        self, db: AsyncSession, department_id: int
    ) -> dict:
        res = {}
        department = await self.cache.get(f"department:{department_id}")
        if department:
            json_department = json.loads(department)
            res["department"] = json_department
        department_record = await self.department_mapper.get_department_by_id(
            db, department_id
        )
        if not department_record:
            res["department"] = None
            return res
        department_data = department_record.to_dict()
        pipe = self.cache.pipeline()
        pipe.set(f"department:{department_id}", json.dumps(department_data))
        pipe.expire(f"department:{department_id}", 60 * 30)
        await pipe.execute()
        res["department"] = department_data

        users = await self.cache.get(f"department_users:{department_id}")
        if users:
            json_users = json.loads(users)
            res["users"] = json_users
            return res
        user_departments = await self.user_department_mapper.get_department_users(
            db, department_id
        )
        user_list = [ud.to_dict() for ud in user_departments]
        pipe = self.cache.pipeline()
        pipe.setex(
            f"department_users:{department_id}",
            60 * 30,
            json.dumps(user_list),
        )
        await pipe.execute()
        res["users"] = user_list
        return res

    async def get_all_departments(self, db: AsyncSession) -> dict:
        cached_departments = await self.cache.get("departments:all")
        if cached_departments:
            json_departments = json.loads(cached_departments)
            return {"departments": json_departments}
        departments = await self.department_mapper.get_all_departments(db)
        department_list = [dept.to_dict() for dept in departments]
        pipe = self.cache.pipeline()
        pipe.setex(
            "departments:all",
            60 * 10,
            json.dumps(department_list),
        )
        await pipe.execute()
        return {"departments": department_list}

    async def create_department(
        self, db: AsyncSession, create_department_request: CreateDepartmentRequest
    ) -> dict:
        department_data = {
            "name": create_department_request.name,
            "parent_id": create_department_request.parent_id,
            "description": create_department_request.description,
        }
        department = await self.department_mapper.insert_department(db, department_data)
        await self.cache.delete("departments:all")
        return {"department": department.to_dict()}

    async def update_department(
        self, db: AsyncSession, department_id: int, update_data: UpdateDepartmentRequest
    ) -> dict:
        update_dict = {
            "name": update_data.name,
            "description": update_data.description,
        }
        department = await self.department_mapper.update_department(
            db, department_id, update_dict
        )
        await self.cache.delete("departments:all")
        await self.cache.delete(f"department:{department_id}")
        return {"department": department.to_dict()}

    async def delete_department(self, db: AsyncSession, department_id: int) -> None:
        await self.department_mapper.delete_department(db, department_id)
        await self.cache.delete("departments:all")
        await self.cache.delete(f"department:{department_id}")
        await self.cache.delete(f"department_users:{department_id}")


def get_department_service(
    cache: redis.Redis = Depends(get_redis_client),
) -> DepartmentService:
    return DepartmentService(cache)
