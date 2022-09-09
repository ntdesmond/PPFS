from fastapi import FastAPI

from . import auth, files, register


def include_routers(app: FastAPI):
    app.include_router(auth.router)
    app.include_router(files.read_router)
    app.include_router(files.write_router)
    app.include_router(register.router)
