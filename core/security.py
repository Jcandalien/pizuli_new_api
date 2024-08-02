from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException,status
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from db.models.user import User
from tortoise.exceptions import DoesNotExist
from tortoise.expressions import Q

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password):
    hashed_password = pwd_context.hash(password)
    # print(f"Hashing password: {password} -> {hashed_password}")
    return hashed_password

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_account(username_or_email: str, password: str):
    try:
        account = await User.get(Q(username=username_or_email) | Q(email=username_or_email))
        if not verify_password(password, account.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password",
            )
        return account
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username or email '{username_or_email}' not found",
        )
