from fastapi import status
from fastapi.responses import ORJSONResponse
from gridfs import NoFile


async def no_file_handler(_, exception: NoFile):
    return ORJSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": exception.__class__.__name__, "detail": str(exception)},
    )
