from fastapi import FastAPI

from settings import settings
from . import auth, files, register


def include_routers(app: FastAPI):
    app.include_router(auth.router)
    app.include_router(files.read_router)
    app.include_router(files.write_router)

    if settings.allow_register:
        app.include_router(register.router)
