from typing import Any
from sqlalchemy import select, update
from model.table.tables.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from model.table.tables.teacher import Teacher
from model.table.tables.student import Student


class AuthMapper:
    async def get_user_by_username(self, db: AsyncSession, username: str):
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        return user

    async def _get_user_by_id(self, db: AsyncSession, user_id: int) -> User:
        result = await db.execute(
            select(User).where(User.id == user_id and User.is_active)
        )
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User:
        result = await db.execute(
            select(User).where(User.id == user_id and User.is_active)
        )
        user = result.scalar_one_or_none()
        return user

    async def get_users_by_ids(
        self, db: AsyncSession, user_ids: list[int]
    ) -> list[User]:
        result = await db.execute(select(User).where(User.id.in_(user_ids)))
        users = result.scalars().all()
        return users

    async def insert_user(
        self, db: AsyncSession, user_data: dict, role: str, no: str
    ) -> User:
        try:
            user = User(**user_data)
            db.add(user)

            await db.flush()

            if role == "teacher":
                profile = Teacher(user_id=user.id, staff_no=no)
            else:
                profile = Student(user_id=user.id, student_no=no)
            db.add(profile)

            await db.commit()
            return user
        except Exception as e:
            await db.rollback()
            raise

    async def update_user_field(
        self, db: AsyncSession, user_id: str, field_name: str, value: Any
    ) -> bool:
        try:
            local_user = await self._get_user_by_id(db, user_id)
            if not hasattr(User, field_name):
                return False

            setattr(local_user, field_name, value)

            await db.commit()

            return True

        except Exception as e:
            await db.rollback()
            raise

    async def update_password(self, db: AsyncSession, user_id: int, password: str):
        await db.execute(
            update(User).where(User.id == user_id).values(password=password)
        )
        return True
