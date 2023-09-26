from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from ..crud.property import PropertyCRUD
from ..schemas.property import (
    PropertyBase,
    PropertyCreate,
    PropertyPatch,
    PropertySchema,
    PropertyUpdate,
)
from ..utils import validate_credentials

router = APIRouter(
    prefix="/property",
    tags=["property"],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}},
    dependencies=[Depends(validate_credentials)],
)


@router.post(
    "/create", response_model=PropertySchema, status_code=status.HTTP_201_CREATED
)
async def create(property: PropertyBase) -> PropertySchema:
    """
    Response Model: PropertySchema
    """
    return await PropertyCRUD.create(PropertyCreate(**dict(property)))


@router.put(
    "/update/{id}", response_model=PropertySchema, status_code=status.HTTP_200_OK
)
async def update(id: str, property: PropertyPatch) -> PropertySchema:
    """
    Response Model: PropertySchema
    """
    # TODO: Property Not Found
    return await PropertyCRUD.update(id, PropertyUpdate(**dict(property)))


@router.delete(
    "/delete/{id}", response_model=bool, status_code=status.HTTP_202_ACCEPTED
)
async def delete(id: str) -> bool:
    """
    Response Model: bool
    """
    # TODO: Property Not Found
    return await PropertyCRUD.delete(id)


@router.get("/", response_model=List[PropertySchema], status_code=status.HTTP_200_OK)
async def get_all() -> List[PropertySchema]:
    """
    Response Model: List[PropertySchema]
    """
    return await PropertyCRUD.get_all()


@router.get("/{id}", response_model=PropertySchema, status_code=status.HTTP_200_OK)
async def get_by_id(id: str) -> PropertySchema:
    """
    Response Model: PropertySchema
    """
    # TODO: Property Not Found
    return await PropertyCRUD.get_by_id(id)


@router.get(
    "/name/{name}", response_model=List[PropertySchema], status_code=status.HTTP_200_OK
)
async def get_by_name(name: str) -> List[PropertySchema]:
    """
    Response Model: List[PropertySchema]
    """
    # TODO: Property Not Found
    return await PropertyCRUD.get_by_name(name)


@router.put(
    "/price/{id}/{price}", response_model=PropertySchema, status_code=status.HTTP_200_OK
)
async def set_price(id: str, price: float) -> PropertySchema:
    """
    Response Model: PropertySchema
    """
    # TODO: Property Not Found
    if price < 0:
        errmsg = f"Price must be positive: {price} < 0"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=errmsg)
    property_patch = PropertyPatch(price=price)
    return await PropertyCRUD.update(id, PropertyUpdate(**dict(property_patch)))
