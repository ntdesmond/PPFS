from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from gridfs import NoFile
from jose import JWTError

from .exceptions.access import NotPrivilegedUser
from .exceptions.auth import InvalidCredentialsError, UserNotFoundError
from .factory import Users, get_user_factory
from .models.dataclasses import TokenData, User, UserRole
from .utils.token import decode_access_token

security = HTTPBearer()

invalid_token_exception = InvalidCredentialsError("Invalid or expired token.")


async def get_access_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> TokenData:
    try:
        return decode_access_token(credentials.credentials)
    except JWTError:
        raise invalid_token_exception


async def get_current_user(
    token_data: TokenData = Depends(get_access_token),
    users: Users = Depends(get_user_factory),
) -> User:
    try:
        return await users.get(ObjectId(token_data.user_id))
    except UserNotFoundError:
        raise invalid_token_exception


async def get_editor_user(user: User = Depends(get_current_user)) -> User:
    # Note: superusers can't modify files
    if not user.role == UserRole.EDITOR:
        raise NotPrivilegedUser("This user cannot modify files.")
    return user


async def get_superuser(user: User = Depends(get_current_user)) -> User:
    if not user.role == UserRole.SUPERUSER:
        raise NotPrivilegedUser("This user cannot add new users.")
    return user


async def get_id(id: str) -> ObjectId:
    try:
        return ObjectId(id)
    except InvalidId:
        raise NoFile("File ID is incorrect")
