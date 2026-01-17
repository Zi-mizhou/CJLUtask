# oss.py
from oss2 import Auth, Bucket
from oss2.exceptions import NotFound, OssError
from fastapi import HTTPException, status
import asyncio
from typing import Optional, BinaryIO
from config.config import settings
from utils.logger import logger

oss_client = None


class AsyncOSSClient:
    def __init__(self):
        # 初始化 auth 和 endpoint
        self.auth = Auth(settings.OSS_ACCESS_KEY_ID, settings.OSS_ACCESS_KEY_SECRET)
        self.endpoint = (
            settings.OSS_ENDPOINT_URL
        )  # 注意：这里应是标准 OSS Endpoint，如 https://oss-cn-hangzhou.aliyuncs.com
        self.bucket_name = settings.OSS_BUCKET_NAME
        self.expire_seconds = settings.OSS_EXPIRE_URL_SECONDS

    def _get_bucket(self) -> Bucket:
        """同步方式创建 bucket 实例（轻量，每次调用都新建也可以）"""
        return Bucket(self.auth, self.endpoint, self.bucket_name)

    async def upload_fileobj(
        self,
        key: str,
        file_obj: BinaryIO,
        headers: Optional[dict] = None,
    ) -> str:
        """异步上传文件对象（内部使用线程池运行同步 oss2 代码）"""
        try:

            def _upload():
                bucket = self._get_bucket()
                bucket.put_object(key, file_obj, headers=headers)
                # 返回公网可访问 URL（假设 bucket 为 public-read）
                return f"https://{self.bucket_name}.{self.endpoint.replace('https://', '')}/{key}"

            url = await asyncio.to_thread(_upload)
            logger.info(f"File uploaded: {url}")
            return url
        except OssError as e:
            logger.error(f"OSS upload error: {e}")
            raise HTTPException(status_code=500, detail="OSS upload failed")

    async def generate_presigned_url(
        self, key: str, expire_seconds: int = None, params: Optional[dict] = None
    ) -> str:
        """生成临时签名 URL（私有文件访问）"""
        if expire_seconds is None:
            expire_seconds = self.expire_seconds
        try:

            def _sign_url():
                bucket = self._get_bucket()
                return bucket.sign_url("GET", key, expire_seconds, params=params)

            url = await asyncio.to_thread(_sign_url)
            return url
        except OssError as e:
            logger.error(f"Presigned URL error: {e}")
            raise HTTPException(status_code=500, detail="Failed to generate URL")

    async def delete_file(self, key: str) -> bool:
        """删除文件"""
        try:

            def _delete():
                bucket = self._get_bucket()
                bucket.delete_object(key)

            await asyncio.to_thread(_delete)
            logger.info(f"Deleted: {key}")
            return True
        except OssError as e:
            logger.error(f"Delete error: {e}")
            return False

    async def file_exists(self, key: str) -> bool:
        """检查文件是否存在"""
        try:

            def _exists():
                bucket = self._get_bucket()
                return bucket.object_exists(key)

            return await asyncio.to_thread(_exists)
        except OssError as e:
            logger.error(f"File exists check error: {e}")
            # 如果网络问题等，保守返回 False 或抛异常
            return False


def get_oss_client() -> AsyncOSSClient:
    global oss_client
    if oss_client is None:
        oss_client = AsyncOSSClient()
    return oss_client
