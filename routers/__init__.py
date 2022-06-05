from fastapi import FastAPI

from settings import settings
from .auth import router as auth_router
from .files import router as files_router
from .register import router as register_router


def include_routers(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(files_router)

    if settings.allow_register:
        app.include_router(register_router)
