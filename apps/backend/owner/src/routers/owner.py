from fastapi import APIRouter, Depends, status

from ..utils import validate_credentials

router = APIRouter(
    prefix="/owner",
    tags=["owner"],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}},
    dependencies=[Depends(validate_credentials)],
)


@router.get("/")
async def get():
    return "Test"
