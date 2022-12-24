from fastapi import APIRouter, status, Depends

from ..models.schemas import UserAuthentication, AuthenticationResponse
from ..utils.token import create_access_token
from ..factory import get_user_factory, Users

router = APIRouter(tags=["Auth"])


@router.post(
    "/register", status_code=status.HTTP_200_OK, response_model=AuthenticationResponse
)
async def register(
    user: UserAuthentication,
    is_admin: bool = False,
    users: Users = Depends(get_user_factory),
):
    user = await users.create(user, is_admin)
    return AuthenticationResponse(access_token=create_access_token(user.id))
