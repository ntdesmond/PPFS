from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .routers import include_routers
from .exceptions import register_error_handlers

app = FastAPI(title="PPFS", version="1.0", default_response_class=ORJSONResponse)

include_routers(app)
register_error_handlers(app)
