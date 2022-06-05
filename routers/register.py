from fastapi import APIRouter

from models.schemas import UserAuthentication
from utils import users, create_access_token

router = APIRouter(tags=["Auth"])


@router.post('/register')
async def register(user: UserAuthentication):
    user = await users.create(user)
    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer"
    }
