# core/security.py
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from base64 import b64decode

from utils.key_manager import get_private_key, get_public_key


async def decrypt_password(encrypted_password: str) -> str:
    """
    使用 RSA 私钥解密前端传来的 Base64 密文
    :param encrypted_password: Base64 编码的密文
    :return: 明文密码
    """

    private_key = await get_private_key()

    encrypted_data = b64decode(encrypted_password)
    decrypted = private_key.decrypt(
        encrypted_data,
        padding.PKCS1v15(),
    )
    return decrypted.decode()


async def encrypt_with_public_key(plain_text: str) -> str:
    """
    使用 RSA 公钥加密明文，返回 Base64 编码的密文
    :param plain_text: 明文字符串
    :return: Base64 编码的密文
    """
    public_key = await get_public_key()

    encrypted = public_key.encrypt(
        plain_text.encode(),
        padding.PKCS1v15(),
    )
    return base64.b64encode(encrypted).decode()
