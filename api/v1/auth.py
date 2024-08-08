from datetime import timedelta
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.security import authenticate_account
from core.security import verify_password, create_access_token
from db.models.franchise import Franchise
from db.models.user import User
from db.schemas.token import Token
from core.security import verify_password, create_access_token, get_password_hash
from db.models.user import User
from db.schemas.token import Token
from db.schemas.user import UserCreate, UserEdit, UserOut
from api.deps import get_current_active_superuser, get_current_user
from tortoise.exceptions import IntegrityError
from tortoise.transactions import in_transaction
from pydantic import ValidationError

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("uvicorn.error")

router = APIRouter()





@router.post("/login", response_model=Token, tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_account(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}




@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate):
    try:
        hashed_password = get_password_hash(user_in.password)
        # print(f"Original password: {user_in.password}, Hashed password: {hashed_password}")  # Debug print
        async with in_transaction():
            user = await User.create(
                username=user_in.username,
                email=user_in.email,
                hashed_password=hashed_password
            )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username or email already exists"
        )
    return user


@router.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        account = await authenticate_account(form_data.username, form_data.password)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(account.id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )



@router.put("/users/me", response_model=UserOut, tags=["Users"])
async def update_user(user_data: UserEdit, current_user: User = Depends(get_current_user)):
    if await User.filter(username=user_data.username).exclude(id=current_user.id).exists():
        raise HTTPException(status_code=400, detail="Username already taken")

    for field, value in user_data.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    await current_user.save()
    return current_user



@router.post("/approve-franchise", status_code=status.HTTP_200_OK)
async def approve_franchise(
    franchise_id: int,
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Approve a franchise. Only accessible by superusers.
    """
    franchise = await Franchise.get_or_none(id=franchise_id)
    if not franchise:
        raise HTTPException(status_code=404, detail="Franchise not found")

    franchise.is_approved = True
    await franchise.save()
    return {"message": "Franchise approved successfully"}