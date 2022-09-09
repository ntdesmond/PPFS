from fastapi import APIRouter, Depends, status

from ..dependencies import get_superuser
from ..factory import Users, get_user_factory
from ..models.dataclasses import UserRole
from ..models.schemas import AuthenticationResponse, UserAuthentication
from ..utils.token import create_access_token

router = APIRouter(tags=["Auth"], dependencies=[Depends(get_superuser)])


@router.post(
    "/register", status_code=status.HTTP_200_OK, response_model=AuthenticationResponse
)
async def register(
    user: UserAuthentication, role: UserRole, users: Users = Depends(get_user_factory)
):
    user = await users.create(user, role)
    return AuthenticationResponse(access_token=create_access_token(user.id))
