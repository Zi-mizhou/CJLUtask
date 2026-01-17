# utils/rsa_keygen.py （仅运行一次）
import asyncio
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pathlib import Path
import aiofiles
from cryptography.hazmat.primitives.asymmetric.types import (
    PrivateKeyTypes,
    PublicKeyTypes,
)

lock = asyncio.Lock()

PUBLIC_KEY = None
PRIVATE_KEY = None


async def create_rsa_keypair():
    key_dir = Path("keys")
    key_dir.mkdir(exist_ok=True)

    private_key_path = key_dir / "private.pem"
    public_key_path = key_dir / "public.pem"

    if private_key_path.exists() and public_key_path.exists():
        return

    # 生成私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048  # 至少 2048 位
    )

    # 序列化私钥（PEM 格式，带密码可选）
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),  # 生产环境建议设密码
    )

    # 生成公钥
    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    async with lock:
        # 保存到文件（或数据库、配置中心）
        async with open(private_key_path, "wb") as f:
            await f.write(pem_private)

        async with open(public_key_path, "wb") as f:
            await f.write(pem_public)


async def refresh_rsa_keypair():
    key_dir = Path("keys")
    key_dir.mkdir(exist_ok=True)

    private_key_path = key_dir / "private.pem"
    public_key_path = key_dir / "public.pem"

    # 生成私钥
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048  # 至少 2048 位
    )

    # 序列化私钥（PEM 格式，带密码可选）
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),  # 生产环境建议设密码
    )

    # 生成公钥
    public_key = private_key.public_key()
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    async with lock:
        # 保存到文件（或数据库、配置中心）
        async with aiofiles.open(private_key_path, "wb") as f:
            await f.write(pem_private)
        async with aiofiles.open(public_key_path, "wb") as f:
            await f.write(pem_public)

        global PUBLIC_KEY
        PUBLIC_KEY = None  # 重置缓存


async def get_public_key() -> str:
    global PUBLIC_KEY
    if PUBLIC_KEY is not None:
        return PUBLIC_KEY
    key_path = Path("keys/public.pem")
    if not key_path.exists():
        raise FileNotFoundError("Public key not found. Please generate keys first.")
    async with lock:
        async with aiofiles.open(key_path, "r") as f:
            PUBLIC_KEY = await f.read()
    return PUBLIC_KEY


async def get_private_key() -> PrivateKeyTypes:
    global PRIVATE_KEY
    if PRIVATE_KEY is not None:
        return PRIVATE_KEY
    key_path = Path("keys/private.pem")
    if not key_path.exists():
        raise FileNotFoundError("Private key not found. Please generate keys first.")
    async with lock:
        async with aiofiles.open(key_path, "rb") as f:
            PRIVATE_KEY = serialization.load_pem_private_key(
                await f.read(), password=None  # 如果私钥有密码，传 bytes
            )
    return PRIVATE_KEY
