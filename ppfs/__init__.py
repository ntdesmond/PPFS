from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .factory import get_user_factory, Users
from .settings import settings
from .routers import include_routers
from .exceptions import register_error_handlers

app = FastAPI(
    title="kiosk-file-server", version="1.0", default_response_class=ORJSONResponse
)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

include_routers(app)
register_error_handlers(app)


@app.on_event("startup")
async def add_default_users():
    users: Users = await get_user_factory()
    await users.clear()
    for user in settings.users:
        await users.create_default(user)
