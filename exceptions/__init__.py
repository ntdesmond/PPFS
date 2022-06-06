from fastapi import FastAPI
from gridfs import NoFile

from .auth import auth_error_handler, AuthError
from .access import access_error_handler, AccessError
from .files import no_file_handler


def register_error_handlers(app: FastAPI):
    app.add_exception_handler(AuthError, auth_error_handler)
    app.add_exception_handler(AccessError, access_error_handler)
    app.add_exception_handler(NoFile, no_file_handler)
