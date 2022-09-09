from bson import ObjectId
from pydantic import BaseModel
from enum import Enum


class UserRole(Enum):
    READONLY = 'read'
    EDITOR = 'edit'
    SUPERUSER = 'admin'


class TokenData(BaseModel):
    user_id: str


class User(BaseModel):
    id: ObjectId
    username: str
    role: UserRole

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
