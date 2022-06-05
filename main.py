from fastapi import FastAPI
from routers import include_routers
from exceptions import register_error_handlers

app = FastAPI(title="PPFS", version="0.0.1")

include_routers(app)
register_error_handlers(app)
