from fastapi import status
from fastapi.responses import ORJSONResponse


class AccessError(Exception):
    pass


class NotPrivilegedUser(AccessError):
    pass


async def access_error_handler(_, exception: AccessError):
    return ORJSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={'detail': str(exception)}
    )
