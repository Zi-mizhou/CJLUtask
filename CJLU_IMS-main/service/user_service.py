import uuid
import redis.asyncio as redis
from fastapi import Depends, UploadFile
from cache.cache import get_redis_client
from mapper.auth_mapper import AuthMapper
from mapper.user_mapper import UserMapper
from model.exception.exceptions.args_exception import ArgsWrongException
from model.exception.exceptions.auth_exception import *
from model.schema.schemas.user import AddUserRequest, UpdateUserProfileRequest
from model.table.tables.user import User as UserTable
import json
from module.oss import get_oss_client
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    def __init__(self, cache: redis.Redis):
        self.cache = cache
        self.user_mapper = UserMapper()
        self.auth_mapper = AuthMapper()

    async def get_user_profile(self, db: AsyncSession, user_id: int, role: str) -> dict:
        user = await self.cache.get(f"user:{user_id}")
        if user:
            json_user = json.loads(user)
            return {"profile": json_user}
        user_profile = await self.user_mapper.get_user_profile_by_user_id(
            db, user_id, role
        )
        if not user_profile:
            raise UserNotExistException()
        user, profile = user_profile
        user_data = UserTable.filter_info({**user.to_dict(), **profile.to_dict()})
        pipe = self.cache.pipeline()
        pipe.set(f"user:{user_id}", json.dumps(user_data))  # 一次性设置所有字段
        pipe.expire(f"user:{user_id}", 60 * 30)  # 为整个 Hash 设置过期时间
        await pipe.execute()
        return {"profile": user_data}

    async def update_user_profile(
        self,
        db: AsyncSession,
        user_id: int,
        role: str,
        profile_data: UpdateUserProfileRequest,
    ) -> None:
        try:
            data = profile_data.profile
        except Exception:
            raise ArgsWrongException()
        await self.user_mapper.update_user_profile(db, user_id, role, data)
        await self.cache.delete(f"user:{user_id}")

    async def upload_avatar(
        self, db: AsyncSession, user_id: int, avatar: UploadFile
    ) -> dict:
        content_type = avatar.content_type
        if content_type == "image/jpeg":
            ext = ".jpg"
        elif content_type == "image/png":
            ext = ".png"
        else:
            raise ArgsWrongException("Unsupported avatar format")
        oss_client = get_oss_client()
        file_obj = avatar.file
        oss_url = await oss_client.upload_fileobj(
            f"avatars/{uuid.uuid4()}_{user_id}{ext}",
            file_obj,
            content_type=content_type,
            headers={"x-oss-object-acl": "public-read"},
        )
        await self.user_mapper.update_user_avatar(db, user_id, oss_url)
        await self.cache.delete(f"user:{user_id}")
        return {"avatar_url": oss_url}

    async def add_user(self, db: AsyncSession, user_data: AddUserRequest) -> dict:
        if user_data.role not in UserTable.ROLE:
            raise RoleNotExistException()
        existing_user = await self.user_mapper.get_user_by_username(
            db, user_data.username
        )
        if existing_user:
            raise UserAlreadyExistsException()
        user_data = {
            "username": user_data.username,
            "password": UserTable.hash_password("cjlu123456"),
            "gender": user_data.gender or "男",
            "name": user_data.name or "",
            "email": user_data.email or "",
            "role": user_data.role,
            "is_active": True,
        }
        new_user = await self.auth_mapper.insert_user(
            db, user_data, user_data.role, no=user_data.username
        )
        user_profile = await self.user_mapper.get_user_profile_by_user_id(
            db, new_user.id, user_data.role
        )
        user, profile = user_profile
        user_data = UserTable.filter_info({**user.to_dict(), **profile.to_dict()})

        return {"user": user_data}

    async def remove_user(self, db: AsyncSession, user_id: int) -> None:
        await self.user_mapper.deactivate_user(db, user_id)
        await self.cache.delete(f"user:{user_id}")


def get_user_service(
    cache: redis.Redis = Depends(get_redis_client),
) -> UserService:
    return UserService(cache)
