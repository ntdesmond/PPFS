from fastapi import APIRouter, status

from models.schemas import UserAuthentication, AuthenticationResponse
from utils.token import create_access_token
from factory import users

router = APIRouter(tags=["Auth"])


@router.post('/auth', status_code=status.HTTP_200_OK, response_model=AuthenticationResponse)
async def login(user: UserAuthentication):
    user = await users.authenticate(user)
    return AuthenticationResponse(access_token=create_access_token(user.id))
