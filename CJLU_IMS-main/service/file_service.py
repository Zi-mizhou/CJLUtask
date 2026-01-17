import asyncio
import json
from pathlib import Path
import uuid
from fastapi import Depends, UploadFile
import redis.asyncio as redis
from cache.cache import get_redis_client
from mapper.file_mapper import FileMapper
from model.exception.exceptions.args_exception import ArgsWrongException
from module.oss import get_oss_client
from sqlalchemy.ext.asyncio import AsyncSession
from utils.logger import logger


class FileService:

    def __init__(self, cache: redis.Redis):
        self.cache = cache
        self.file_mapper = FileMapper()

    async def get_file_list(self, db: AsyncSession, parent_id: int = None) -> dict:
        if parent_id is None:
            cached_files = await self.cache.get("file_list:root")
        else:
            cached_files = await self.cache.get(f"file_list:{parent_id}")
        if cached_files:
            json_files = json.loads(cached_files)
            return {"files": json_files}
        files = await self.file_mapper.get_file_list(db, parent_id)
        file_list = [file.to_dict() for file in files]
        pipe = self.cache.pipeline()
        pipe.setex(
            f"file_list:{parent_id if parent_id is not None else 'root'}",
            60 * 10,
            json.dumps(file_list),
        )
        await pipe.execute()
        return {"files": file_list}

    async def create_folder(
        self, db: AsyncSession, folder_name: str, parent_id: int = None
    ) -> dict:
        file_data = {
            "name": folder_name,
            "type": "directory",
            "parent": parent_id,
            "url": "",
            "size": 0,
            "is_dir": 1,
        }
        file = await self.file_mapper.upload_file(db, file_data)
        await self.cache.delete(
            f"file_list:{parent_id if parent_id is not None else 'root'}"
        )
        return {"file": file.to_dict()}

    async def upload_file(
        self, db: AsyncSession, file: UploadFile = None, parent_id: int = None
    ) -> dict:
        ext = Path(file.filename).suffix.lower()
        if ext not in {
            ".jpg",
            ".jpeg",
            ".png",
            ".pdf",
            ".doc",
            ".docx",
            ".xls",
            ".xlsx",
            ".ppt",
            ".pptx",
            ".txt",
            ".zip",
            ".rar",
            ".mp3",
            ".mp4",
        }:  # 按需扩展
            raise ArgsWrongException()
        key = f"files/{uuid.uuid4().hex}{ext}"
        oss_client = get_oss_client()
        oss_url = await oss_client.upload_fileobj(
            key, file.file, headers={"Content-Type": file.content_type}
        )

        file_data = {
            "name": file.filename,
            "type": file.content_type,
            "parent": parent_id,
            "url": oss_url,
            "size": file.size,
            "is_dir": 0,
            "key": key,
            "public": 0,
        }
        file = await self.file_mapper.upload_file(db, file_data)
        await self.cache.delete(
            f"file_list:{parent_id if parent_id is not None else 'root'}"
        )
        return {"file": file.to_dict()}

    async def delete_file_list(
        self, db: AsyncSession, file_ids: list[int], parent_id: int = None
    ) -> None:
        file_list = await self.file_mapper.get_files_by_ids(db, file_ids)

        async def delete_oss_files():
            oss_client = get_oss_client()
            for file in file_list:
                if not file.is_dir:
                    await oss_client.delete_file(file.key)

        asyncio.create_task(delete_oss_files())
        await self.file_mapper.delete_file_list(db, file_ids)
        # Invalidate all cached file lists since we don't know the parent
        await self.cache.delete(
            f"file_list:{parent_id if parent_id is not None else 'root'}"
        )

    async def get_download_url_list(
        self, db: AsyncSession, file_ids: list[int]
    ) -> dict:
        download_urls = []

        no_cache_file_ids = []
        for file_id in file_ids:
            cache_url = await self.cache.get(f"file_download_url:{file_id}")
            if cache_url:
                download_urls.append({"id": file_id, "url": cache_url})
                continue
            no_cache_file_ids.append(file_id)

        if no_cache_file_ids:
            oss_client = get_oss_client()
            file_list = await self.file_mapper.get_files_by_ids(db, no_cache_file_ids)
            for file in file_list:
                if file.is_dir:
                    continue
                if file.public == 1:
                    download_url = file.url
                else:
                    download_url = await oss_client.generate_presigned_url(
                        file.key, expire_seconds=300
                    )
                download_urls.append({"id": file.id, "url": download_url})
                await self.cache.setex(
                    f"file_download_url:{file.id}", 290, download_url
                )

        return {"download_urls": download_urls}

    async def rename_file(self, db: AsyncSession, file_id: int, new_name: str) -> dict:
        file = await self.file_mapper.get_file_by_id(db, file_id)
        if not file:
            raise ArgsWrongException()
        file.name = new_name
        await self.file_mapper.update_file(db, file)
        await self.cache.delete(
            f"file_list:{file.parent if file.parent is not None else 'root'}"
        )
        return {"file": file.to_dict()}

    async def preview_file(self, db: AsyncSession, file_id: int) -> dict:
        file = await self.file_mapper.get_file_by_id(db, file_id)
        if not file or file.is_dir:
            raise ArgsWrongException()
        oss_client = get_oss_client()
        if file.public == 1:
            preview_url = file.url
        else:
            logger.info(f"Generating preview URL for file key: {file.key}")
            preview_url = await oss_client.generate_presigned_url(
                file.key,
                expire_seconds=300,
                params={"response-content-disposition": "inline"},
            )
        return {"preview_url": preview_url, "file_name": file.name}


def get_file_service(
    cache: redis.Redis = Depends(get_redis_client),
) -> FileService:
    return FileService(cache)
