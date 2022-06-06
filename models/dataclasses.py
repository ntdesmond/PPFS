from bson import ObjectId
from pydantic import BaseModel, Field


class TokenData(BaseModel):
    user_id: str


class User(BaseModel):
    id: ObjectId
    username: str
    is_admin: bool

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
