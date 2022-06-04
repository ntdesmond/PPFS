from fastapi import APIRouter

from utils.token import create_access_token
from schemas import UserAuthentication

router = APIRouter()


@router.post('/auth')
async def login(user: UserAuthentication):
    return {
        "access_token": create_access_token(user.username),
        "token_type": "bearer"
    }
