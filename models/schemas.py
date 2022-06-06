from bson import ObjectId
from pydantic import BaseModel, constr


class UserAuthentication(BaseModel):
    username: constr(min_length=3, max_length=32, strip_whitespace=True)
    password: constr(min_length=8, max_length=64)


class AuthenticationResponse(BaseModel):
    access_token: str


class FileInfo(BaseModel):
    id: str
    filename: str
    content_type: str

    def __init__(self, id: ObjectId | str, **kwargs):
        super().__init__(id=str(id), **kwargs)
