from datetime import datetime, timedelta

from bson import ObjectId
from jose import jwt

from models.dataclasses import TokenData
from settings import settings


def create_access_token(user_id: ObjectId, expires_in: timedelta | None = None):
    token_data = {
        "user": str(user_id),
        "exp": datetime.utcnow() + (expires_in if expires_in is not None else timedelta(minutes=15))
    }
    return jwt.encode(token_data, key=settings.jwt_key, algorithm="HS256")


def decode_access_token(token: str) -> TokenData:
    return TokenData(user_id=jwt.decode(token, key=settings.jwt_key, algorithms=["HS256"]).get("user"))
