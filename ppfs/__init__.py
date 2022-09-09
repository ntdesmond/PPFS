from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .factory import get_user_factory, Users
from .models.schemas import UserAuthentication
from .settings import settings
from .routers import include_routers
from .exceptions import register_error_handlers

app = FastAPI(title="PPFS", version="1.0", default_response_class=ORJSONResponse)

include_routers(app)
register_error_handlers(app)


@app.on_event("startup")
async def add_default_superuser():
    users: Users = await get_user_factory()
    await users.create_default_superuser(
        UserAuthentication(
            username=settings.default_superuser_name,
            password=settings.default_superuser_password
        )
    )
