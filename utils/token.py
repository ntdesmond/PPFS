from datetime import datetime, timedelta
from jose import jwt

from settings import settings


def create_access_token(username: str, expires_in: timedelta | None = None):
    token_data = {
        "user": username,
        "exp": datetime.utcnow() + (expires_in if expires_in is not None else timedelta(minutes=15))
    }
    return jwt.encode(token_data, key=settings.jwt_key, algorithm="HS256")


def check_access_token(token: str) -> str | None:
    return jwt.decode(token, key=settings.jwt_key, algorithms=["HS256"]).get("user")
