from fastapi import APIRouter, Depends, status

from ..factory import Users, get_user_factory
from ..models.schemas import AuthenticationResponse, UserAuthentication
from ..utils.token import create_access_token

router = APIRouter(tags=["Auth"])


@router.post(
    "/auth", status_code=status.HTTP_200_OK, response_model=AuthenticationResponse
)
async def login(user: UserAuthentication, users: Users = Depends(get_user_factory)):
    user = await users.authenticate(user)
    return AuthenticationResponse(access_token=create_access_token(user.id))
