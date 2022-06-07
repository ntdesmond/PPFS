from fastapi import APIRouter, status, Depends

from ..models.schemas import UserAuthentication, AuthenticationResponse
from ..utils.token import create_access_token
from ..factory import get_user_factory, Users

router = APIRouter(tags=["Auth"])


@router.post('/auth', status_code=status.HTTP_200_OK, response_model=AuthenticationResponse)
async def login(user: UserAuthentication, users: Users = Depends(get_user_factory)):
    user = await users.authenticate(user)
    return AuthenticationResponse(access_token=create_access_token(user.id))
