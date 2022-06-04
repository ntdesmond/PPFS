from fastapi import Security, HTTPException, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, ExpiredSignatureError

from schemas import TokenData
from utils.token import check_access_token

security = HTTPBearer()


async def get_access_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> TokenData:
    try:
        return TokenData(user=check_access_token(credentials.credentials))
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(token_data: TokenData = Depends(get_access_token)) -> str:
    # TODO: check the validity of the user
    return token_data.user
