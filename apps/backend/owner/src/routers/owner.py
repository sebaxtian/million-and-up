from typing import List

from fastapi import APIRouter, Depends, status

from ..crud.owner import OwnerCRUD
from ..schemas.owner import OwnerBase, OwnerCreate, OwnerPatch, OwnerSchema, OwnerUpdate
from ..utils import validate_credentials

router = APIRouter(
    prefix="/owner",
    tags=["owner"],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}},
    dependencies=[Depends(validate_credentials)],
)


@router.post("/create", response_model=OwnerSchema, status_code=status.HTTP_201_CREATED)
async def create(owner: OwnerBase) -> OwnerSchema:
    """
    Response Model: OwnerSchema
    """
    return await OwnerCRUD.create(OwnerCreate(**dict(owner)))


@router.put("/update/{id}", response_model=OwnerSchema, status_code=status.HTTP_200_OK)
async def update(id: str, owner: OwnerPatch) -> OwnerSchema:
    """
    Response Model: OwnerSchema
    """
    # TODO: Owner Not Found
    return await OwnerCRUD.update(id, OwnerUpdate(**dict(owner)))


@router.delete(
    "/delete/{id}", response_model=bool, status_code=status.HTTP_202_ACCEPTED
)
async def delete(id: str) -> bool:
    """
    Response Model: bool
    """
    # TODO: Owner Not Found
    return await OwnerCRUD.delete(id)


@router.get("/", response_model=List[OwnerSchema], status_code=status.HTTP_200_OK)
async def get_all() -> List[OwnerSchema]:
    """
    Response Model: List[OwnerSchema]
    """
    return await OwnerCRUD.get_all()


@router.get("/{id}", response_model=OwnerSchema, status_code=status.HTTP_200_OK)
async def get_by_id(id: str) -> OwnerSchema:
    """
    Response Model: OwnerSchema
    """
    # TODO: Owner Not Found
    return await OwnerCRUD.get_by_id(id)


@router.get(
    "/name/{name}", response_model=List[OwnerSchema], status_code=status.HTTP_200_OK
)
async def get_by_name(name: str) -> List[OwnerSchema]:
    """
    Response Model: List[OwnerSchema]
    """
    # TODO: Owner Not Found
    return await OwnerCRUD.get_by_name(name)
