from datetime import datetime, timedelta, timezone
import jwt

from config.config import settings
from model.schema.schemas.user import User


def create_jwt_token(user: User) -> str:
    now_utc = datetime.now(timezone.utc)
    payload = {
        "id": user.id,
        "role": user.role,
        "exp": now_utc + timedelta(days=7),  # 过期时间：7天
        "iat": now_utc,  # 签发时间
    }
    token = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return token
