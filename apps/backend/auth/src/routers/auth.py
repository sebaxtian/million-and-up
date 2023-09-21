from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..schemas.user import UserSchema
from ..utils import get_current_active_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}},
)


@router.get("/users/me/", response_model=UserSchema)
async def users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)]
):
    """
    Current User
    """
    return current_user
