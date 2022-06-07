from bson.errors import InvalidId
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Security, Depends
from gridfs import NoFile
from jose import JWTError
from bson import ObjectId

from .exceptions.auth import InvalidCredentialsError, UserNotFoundError
from .exceptions.access import NotPrivilegedUser
from .models.dataclasses import TokenData, User
from .utils.token import decode_access_token
from .factory import get_user_factory, Users

security = HTTPBearer()

invalid_token_exception = InvalidCredentialsError("Invalid or expired token.")


async def get_access_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> TokenData:
    try:
        return decode_access_token(credentials.credentials)
    except JWTError:
        raise invalid_token_exception


async def get_current_user(
    token_data: TokenData = Depends(get_access_token),
    users: Users = Depends(get_user_factory)
) -> User:
    try:
        return await users.get(ObjectId(token_data.user_id))
    except UserNotFoundError:
        raise invalid_token_exception


async def get_privileged_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise NotPrivilegedUser("This user cannot modify files.")
    return user


async def get_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except InvalidId:
        raise NoFile("File ID is incorrect")
