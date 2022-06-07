from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .factory import get_user_factory, Users
from .settings import settings
from .routers import include_routers
from .exceptions import register_error_handlers

app = FastAPI(title="PPFS", version="1.0", default_response_class=ORJSONResponse)

include_routers(app)
register_error_handlers(app)


@app.on_event("startup")
async def add_default_users():
    if settings.allow_register:
        return

    users = await get_user_factory()
    await users.create_default(settings.admin_credentials, is_admin=True)
    await users.create_default(settings.user_credentials, is_admin=False)
