from fastapi import FastAPI

from .auth import auth_error_handler, AuthError


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(AuthError, auth_error_handler)