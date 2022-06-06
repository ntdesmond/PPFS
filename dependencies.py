from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security, Depends
from jose import JWTError
from bson import ObjectId

from exceptions.auth import InvalidCredentialsError, UserNotFoundError
from models.dataclasses import TokenData, User
from utils.token import decode_access_token
from factory import users

security = HTTPBearer()

invalid_token_exception = InvalidCredentialsError("Invalid or expired token.")


async def get_access_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> TokenData:
    try:
        return decode_access_token(credentials.credentials)
    except JWTError:
        raise invalid_token_exception


async def get_current_user(token_data: TokenData = Depends(get_access_token)) -> User:
    try:
        return await users.get(ObjectId(token_data.user_id))
    except UserNotFoundError:
        raise invalid_token_exception
