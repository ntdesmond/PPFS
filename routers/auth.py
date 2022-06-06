from fastapi import APIRouter

from models.schemas import UserAuthentication
from utils.token import create_access_token
from factory import users

router = APIRouter(tags=["Auth"])


@router.post('/auth')
async def login(user: UserAuthentication):
    user = await users.authenticate(user)
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer"
    }
