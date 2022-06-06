from fastapi import FastAPI

from .auth import auth_error_handler, AuthError
from .access import access_error_handler, AccessError


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(AuthError, auth_error_handler)
    app.add_exception_handler(AccessError, access_error_handler)