from bson import ObjectId
from pydantic import BaseModel, constr


class UserAuthentication(BaseModel):
    username: constr(min_length=3, max_length=32, strip_whitespace=True)
    password: constr(min_length=8, max_length=64)


class FileInfo(BaseModel):
    id: ObjectId
    filename: str
    content_type: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }