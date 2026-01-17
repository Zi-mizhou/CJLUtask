from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from model.table.tables.user_department import UserDepartment


class UserDepartmentMapper:
    async def get_user_department(self, db: AsyncSession, user_id: int):
        stmt = select(UserDepartment).where(UserDepartment.user_id == user_id)
        result = await db.execute(stmt)
        user_department = result.scalar_one_or_none()
        return user_department

    async def get_department_users(self, db: AsyncSession, department_id: int):
        stmt = select(UserDepartment).where(
            UserDepartment.department_id == department_id
        )
        result = await db.execute(stmt)
        user_departments = result.scalars().all()
        return user_departments

    async def update_user_department(
        self, db: AsyncSession, user_id: int, department_id: int
    ):
        try:
            stmt = select(UserDepartment).where(UserDepartment.user_id == user_id)
            result = await db.execute(stmt)
            user_department = result.scalar_one_or_none()
            if user_department:
                user_department.department_id = department_id
            else:
                user_department = UserDepartment(
                    user_id=user_id, department_id=department_id
                )
                db.add(user_department)

            await db.commit()
            return user_department
        except Exception as e:
            await db.rollback()
            raise

    async def delete_user_department(self, db: AsyncSession, user_id: int):
        try:
            stmt = (
                update(UserDepartment)
                .where(UserDepartment.user_id == user_id)
                .values(is_active=1)
            )
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise
