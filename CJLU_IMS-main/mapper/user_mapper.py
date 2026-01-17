from sqlalchemy import select
from model.table.tables.student import Student
from sqlalchemy.ext.asyncio import AsyncSession

from model.table.tables.teacher import Teacher
from model.table.tables.user import User


class UserMapper:
    async def get_user_profile_by_user_id(
        self, db: AsyncSession, user_id: int, role: str
    ):
        if role == "teacher":
            return await self.get_teacher_profile_by_user_id(db, user_id)
        else:
            return await self.get_student_profile_by_user_id(db, user_id)

    async def get_student_profile_by_user_id(self, db: AsyncSession, user_id: int):
        stmt = (
            select(User, Student)
            .join(Student, User.id == Student.user_id)
            .where(User.id == user_id)
        )
        result = await db.execute(stmt)
        user_profile = result.fetchone()
        return user_profile

    async def get_teacher_profile_by_user_id(self, db: AsyncSession, user_id: int):
        stmt = (
            select(User, Teacher)
            .join(Teacher, User.id == Teacher.user_id)
            .where(User.id == user_id)
        )
        result = await db.execute(stmt)
        user_profile = result.fetchone()
        return user_profile

    async def update_user_profile(
        self, db: AsyncSession, user_id: int, role: str, profile_data: dict
    ):
        try:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                for key, value in profile_data.items():
                    setattr(user, key, value)
            if role == "teacher":
                await self.update_teacher_profile(db, user_id, profile_data)
            else:
                await self.update_student_profile(db, user_id, profile_data)

            await db.commit()
        except Exception as e:
            await db.rollback()
            raise

    async def update_user_avatar(self, db: AsyncSession, user_id: int, avatar_url: str):
        try:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                user.avatar_url = avatar_url
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise

    async def update_student_profile(
        self, db: AsyncSession, user_id: int, profile_data: dict
    ):
        stmt = select(Student).where(Student.user_id == user_id)
        result = await db.execute(stmt)
        student = result.scalar_one_or_none()
        if student:
            for key, value in profile_data.items():
                setattr(student, key, value)

    async def update_teacher_profile(
        self, db: AsyncSession, user_id: int, profile_data: dict
    ):
        stmt = select(Teacher).where(Teacher.user_id == user_id)
        result = await db.execute(stmt)
        teacher = result.scalar_one_or_none()
        if teacher:
            for key, value in profile_data.items():
                setattr(teacher, key, value)

    async def deactivate_user(self, db: AsyncSession, user_id: int):
        try:
            stmt = select(User).where(User.id == user_id)
            result = await db.execute(stmt)
            user = result.scalar_one_or_none()
            if user:
                user.is_active = False
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise
