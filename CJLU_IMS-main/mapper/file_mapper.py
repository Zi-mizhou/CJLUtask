from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from model.table.tables.file import File


class FileMapper:
    async def get_file_by_id(self, db: AsyncSession, file_id: int):
        stmt = select(File).where(File.id == file_id, File.active == 1)
        result = await db.execute(stmt)
        file = result.scalar_one_or_none()
        return file

    async def get_files_by_ids(self, db: AsyncSession, file_ids: list[int]):
        stmt = select(File).where(File.id.in_(file_ids), File.active == 1)
        result = await db.execute(stmt)
        files = result.scalars().all()
        return files

    async def get_file_list(self, db: AsyncSession, parent_id: int = None):
        if parent_id is None:
            stmt = select(File).where(File.parent.is_(None), File.active == 1)
            result = await db.execute(stmt)
            files = result.scalars().all()
            return files
        else:
            stmt = select(File).where(File.parent == parent_id, File.active == 1)
            result = await db.execute(stmt)
            files = result.scalars().all()
            return files

    async def upload_file(self, db: AsyncSession, file_data: dict):
        try:
            file = File(**file_data)
            db.add(file)
            await db.commit()
            return file
        except Exception as e:
            await db.rollback()
            raise

    async def delete_file(self, db: AsyncSession, file_id: int):
        try:
            stmt = update(File).where(File.id == file_id).values(active=0)
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise

    async def delete_file_list(self, db: AsyncSession, file_ids: list[int]):
        try:
            stmt = update(File).where(File.id.in_(file_ids)).values(active=0)
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise

    async def delete_files_by_parent(self, db: AsyncSession, parent_id: int):
        try:
            stmt = update(File).where(File.parent == parent_id).values(active=0)
            await db.execute(stmt)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise

    async def update_file(self, db: AsyncSession, file: File):
        try:
            db.add(file)
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise
