from typing import List

from fastapi import APIRouter, Depends, status

from ..crud.property_trace import PropertyTraceCRUD
from ..schemas.property_trace import (
    PropertyTraceBase,
    PropertyTraceCreate,
    PropertyTracePatch,
    PropertyTraceSchema,
    PropertyTraceUpdate,
)
from ..utils import validate_credentials

router = APIRouter(
    prefix="/property_trace",
    tags=["property_trace"],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}},
    dependencies=[Depends(validate_credentials)],
)


@router.post(
    "/create", response_model=PropertyTraceSchema, status_code=status.HTTP_201_CREATED
)
async def create(property_trace: PropertyTraceBase) -> PropertyTraceSchema:
    """
    Response Model: PropertyTraceSchema
    """
    return await PropertyTraceCRUD.create(PropertyTraceCreate(**dict(property_trace)))


@router.put(
    "/update/{id}", response_model=PropertyTraceSchema, status_code=status.HTTP_200_OK
)
async def update(id: str, property_trace: PropertyTracePatch) -> PropertyTraceSchema:
    """
    Response Model: PropertyTraceSchema
    """
    # TODO: PropertyTrace Not Found
    return await PropertyTraceCRUD.update(
        id, PropertyTraceUpdate(**dict(property_trace))
    )


@router.delete(
    "/delete/{id}", response_model=bool, status_code=status.HTTP_202_ACCEPTED
)
async def delete(id: str) -> bool:
    """
    Response Model: bool
    """
    # TODO: PropertyTrace Not Found
    return await PropertyTraceCRUD.delete(id)


@router.get(
    "/", response_model=List[PropertyTraceSchema], status_code=status.HTTP_200_OK
)
async def get_all() -> List[PropertyTraceSchema]:
    """
    Response Model: List[PropertyTraceSchema]
    """
    return await PropertyTraceCRUD.get_all()


@router.get("/{id}", response_model=PropertyTraceSchema, status_code=status.HTTP_200_OK)
async def get_by_id(id: str) -> PropertyTraceSchema:
    """
    Response Model: PropertyTraceSchema
    """
    # TODO: PropertyTrace Not Found
    return await PropertyTraceCRUD.get_by_id(id)


@router.get(
    "/name/{name}",
    response_model=List[PropertyTraceSchema],
    status_code=status.HTTP_200_OK,
)
async def get_by_name(name: str) -> List[PropertyTraceSchema]:
    """
    Response Model: List[PropertyTraceSchema]
    """
    # TODO: PropertyTrace Not Found
    return await PropertyTraceCRUD.get_by_name(name)
