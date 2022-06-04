from fastapi import FastAPI
from routers import files, auth

app = FastAPI(title="PPFS", version="0.0.1")
app.include_router(files.router)
app.include_router(auth.router)