from fastapi import status
from fastapi.responses import ORJSONResponse


class AuthError(Exception):
    pass


class InvalidCredentialsError(AuthError):
    pass


class UserNotFoundError(AuthError):
    pass


async def auth_error_handler(_, exception: AuthError):
    return ORJSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": exception.__class__.__name__, "detail": str(exception)},
        headers={"WWW-Authenticate": "Bearer"},
    )
