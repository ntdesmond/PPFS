from fastapi import FastAPI
from routers import files, auth, register
from settings import settings

app = FastAPI(title="PPFS", version="0.0.1")

app.include_router(files.router)
app.include_router(auth.router)
if settings.allow_register:
    app.include_router(register.router)
