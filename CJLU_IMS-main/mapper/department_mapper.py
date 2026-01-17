from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from model.table.tables.department import Department


class DepartmentMapper:
    async def get_department_by_id(self, db: AsyncSession, department_id: int):
        stmt = select(Department).where(
            Department.id == department_id and Department.is_active == 1
        )
        result = await db.execute(stmt)
        department = result.scalar_one_or_none()
        return department

    async def get_all_departments(self, db: AsyncSession):
        stmt = select(Department).where(Department.is_active == 1)
        result = await db.execute(stmt)
        departments = result.scalars().all()
        return departments

    async def insert_department(self, db: AsyncSession, department_data: dict):
        try:
            department = Department(**department_data)
            db.add(department)
            await db.commit()
            return department
        except Exception as e:
            await db.rollback()
            raise

    async def update_department(
        self, db: AsyncSession, department_id: int, update_data: dict
    ):
        try:
            stmt = select(Department).where(Department.id == department_id)
            result = await db.execute(stmt)
            department = result.scalar_one_or_none()
            if department:
                for key, value in update_data.items():
                    setattr(department, key, value)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise

    async def delete_department(self, db: AsyncSession, department_id: int):
        try:
            stmt = (
                update(Department)
                .where(Department.id == department_id)
                .values(is_active=0)
            )
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise
