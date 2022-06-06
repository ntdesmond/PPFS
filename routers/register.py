from fastapi import APIRouter, status

from models.schemas import UserAuthentication, AuthenticationResponse
from utils.token import create_access_token
from factory import users

router = APIRouter(tags=["Auth"])


@router.post('/register', status_code=status.HTTP_200_OK, response_model=AuthenticationResponse)
async def register(user: UserAuthentication, is_admin: bool = False):
    user = await users.create(user, is_admin)
    return AuthenticationResponse(access_token=create_access_token(user.id))
