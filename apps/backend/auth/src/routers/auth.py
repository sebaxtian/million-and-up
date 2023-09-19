from datetime import timedelta
from typing import Annotated

from config.settings import settings
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import TokenSchema
from schemas.user import UserSchema
from utils import (authenticate_user, create_access_token,
                   get_current_active_user)

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(get_current_active_user)],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}},
)


@router.post("/login", response_model=TokenSchema)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login to get Token using the OAuth2PasswordRequestForm built-in form FastAPI
    TODO: Update to use OAuth2 scopes instead of "role" Token payload attribute
    https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    # Create Token
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserSchema)
async def users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)]
):
    """
    Current User
    """
    return current_user
