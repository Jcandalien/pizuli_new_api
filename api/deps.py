import logging
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import UUID4, ValidationError
from core.config import ALGORITHM, SECRET_KEY
from db.models.franchise import Franchise
from db.models.user import User
from jose import JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger(__name__)
security = HTTPBearer()

security = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        logger.debug(f"Received token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Decoded payload: {payload}")
        user_id: str = payload.get("sub")
        if user_id is None:
            logger.error("Token payload does not contain 'sub' claim")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError as e:
        logger.error(f"Failed to decode token: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user = await User.get_or_none(id=user_id)
    if user is None:
        logger.error(f"User with id {user_id} not found in database")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


async def get_current_active_superuser(current_user: User = Depends(get_current_active_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    return current_user


async def get_approved_franchise(
    franchise_id: UUID4,
    current_user: User = Depends(get_current_active_user)
) -> Franchise:
    franchise = await Franchise.get_or_none(id=franchise_id, owner=current_user)
    if not franchise:
        raise HTTPException(status_code=404, detail="Franchise not found")
    if not franchise.is_approved:
        raise HTTPException(status_code=403, detail="Franchise is not approved")
    return franchise