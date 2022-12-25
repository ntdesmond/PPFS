from bson import ObjectId
from pydantic import BaseModel, constr


class UserAuthentication(BaseModel):
    username: constr(min_length=3, max_length=32, strip_whitespace=True)
    password: constr(min_length=8, max_length=64)


class AuthenticationResponse(BaseModel):
    access_token: str


class FileDescription(BaseModel):
    ru: str
    en: str

    @classmethod
    def from_filename(cls, filename: str):
        description = filename.rsplit(".", maxsplit=1)[0]
        return cls(ru=description, en=description)


class OptionalFileDescription(FileDescription):
    ru: str | None
    en: str | None


class FileInfo(BaseModel):
    id: str
    filename: str
    content_type: str
    description: FileDescription

    def __init__(self, id: ObjectId | str, **kwargs):
        super().__init__(id=str(id), **kwargs)
