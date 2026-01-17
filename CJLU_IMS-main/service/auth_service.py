import time
import uuid
from fastapi import Depends
from cache.cache import get_redis_client
from mapper.auth_mapper import AuthMapper
from mapper.user_mapper import UserMapper
import redis.asyncio as redis
from model.exception.exceptions.auth_exception import *
from model.table.tables.user import User as UserTable
from utils.key_manager import get_public_key, refresh_rsa_keypair
from utils.jwt_utils import create_jwt_token
from utils.rsa import decrypt_password
import base64
from utils.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession


class AuthService:
    def __init__(self, cache: redis.Redis):
        self.cache = cache
        self.auth_mapper = AuthMapper()
        self.user_mapper = UserMapper()

    async def login(self, db: AsyncSession, username: str, password: str) -> dict:
        user = await self.auth_mapper.get_user_by_username(db, username)
        if not user:
            raise UserNotExistException()
        decode_password = await decrypt_password(password)
        if not user.verify_password(decode_password):
            raise PasswordErrorException()

        role = user.role
        if role not in UserTable.ROLE:
            raise RoleNotExistException()
        if role == "teacher":
            user_profile = await self.user_mapper.get_teacher_profile_by_user_id(
                db, user.id
            )
        else:
            user_profile = await self.user_mapper.get_student_profile_by_user_id(
                db, user.id
            )

        user, profile = user_profile
        user_data = UserTable.filter_info({**user.to_dict(), **profile.to_dict()})

        return {"token": create_jwt_token(user), "user": user_data}

    async def register(
        self, db: AsyncSession, username: str, password: str, role: str
    ) -> dict:
        if role not in UserTable.ROLE:
            raise RoleNotExistException()

        existing_user = await self.auth_mapper.get_user_by_username(db, username)
        if existing_user:
            raise UserAlreadyExistsException()

        decode_password = await decrypt_password(password)
        user_data = {
            "username": username,
            "password": UserTable.hash_password(decode_password),
            "role": role,
            "gender": "男",
            "is_active": True,
        }
        new_user = await self.auth_mapper.insert_user(
            db, user_data, role=role, no=username
        )
        user_profile = await self.user_mapper.get_user_profile_by_user_id(
            db, new_user.id, role
        )
        user, profile = user_profile
        user_data = UserTable.filter_info({**user.to_dict(), **profile.to_dict()})

        return {"token": create_jwt_token(new_user), "user": user_data}

    async def reset_password(
        self, db: AsyncSession, user_id: int, old_password: str, new_password: str
    ) -> dict:
        if old_password == new_password:
            raise OldNewException()
        user = await self.auth_mapper.get_user_by_id(db, user_id)
        if not user:
            raise UserNotExistException()

        if not user.verify_password(old_password):
            raise PasswordErrorException()

        hashed_password = UserTable.hash_password(new_password)

        await self.auth_mapper.update_user_field(
            db, user_id, "password", hashed_password
        )

        return {}

    async def get_public_key(self, pas: bool) -> tuple[str, str, str]:
        public_key = await get_public_key()
        public_key_b64 = base64.b64encode(public_key.encode("utf-8")).decode()
        if pas:
            return public_key_b64, "", ""
        session_id = uuid.uuid4().hex
        timestamp = str(time.time()) + "_" + uuid.uuid4().hex[-4:]
        redis_key = f"session:{timestamp}"
        await self.cache.setex(redis_key, 60 * 60, session_id)
        return public_key_b64, session_id, timestamp

    async def refresh_public_key(self, user_id: int, role: str) -> None:
        if role != "admin":
            raise PermissionDeniedException()
        logger.warning(
            f'{time.strftime("%Y-%m-%d %H:%M:%S")}: {user_id} requested RSA key pair refresh'
        )
        await refresh_rsa_keypair()


def get_auth_service(
    cache: redis.Redis = Depends(get_redis_client),
) -> AuthService:
    return AuthService(cache)
