from fastapi import APIRouter

from schemas import UserAuthentication

router = APIRouter()


@router.post('/register')
async def register(user: UserAuthentication):
    return {"reg": "not yet"}
