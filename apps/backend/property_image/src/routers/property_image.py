from typing import Annotated, List

from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from ..config.settings import settings
from ..crud.property_image import PropertyImageCRUD
from ..schemas.property_image import (
    PropertyImageBase,
    PropertyImageCreate,
    PropertyImagePatch,
    PropertyImageSchema,
    PropertyImageUpdate,
)
from ..utils import validate_credentials

router = APIRouter(
    prefix="/property_image",
    tags=["property_image"],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "Not Found"}},
    dependencies=[Depends(validate_credentials)],
)


@router.post(
    "/create", response_model=PropertyImageSchema, status_code=status.HTTP_201_CREATED
)
async def create(
    id_property: Annotated[str, Form()], file: Annotated[UploadFile, File()]
) -> PropertyImageSchema:
    """
    Response Model: PropertyImageSchema
    """
    content = await file.read()
    with open(f"{settings.path_images}/{file.filename}", "wb") as f:
        f.write(content)
        f.close()
    property_image = PropertyImageBase(id_property=id_property, filename=file.filename)
    # TODO: Check PropertyID
    return await PropertyImageCRUD.create(PropertyImageCreate(**dict(property_image)))


@router.put(
    "/update/{id}", response_model=PropertyImageSchema, status_code=status.HTTP_200_OK
)
async def update(id: str, property_image: PropertyImagePatch) -> PropertyImageSchema:
    """
    Response Model: PropertyImageSchema
    """
    # TODO: PropertyImage Not Found
    return await PropertyImageCRUD.update(
        id, PropertyImageUpdate(**dict(property_image))
    )


@router.delete(
    "/delete/{id}", response_model=bool, status_code=status.HTTP_202_ACCEPTED
)
async def delete(id: str) -> bool:
    """
    Response Model: bool
    """
    # TODO: PropertyImage Not Found
    return await PropertyImageCRUD.delete(id)


@router.get(
    "/", response_model=List[PropertyImageSchema], status_code=status.HTTP_200_OK
)
async def get_all() -> List[PropertyImageSchema]:
    """
    Response Model: List[PropertyImageSchema]
    """
    return await PropertyImageCRUD.get_all()


@router.get("/{id}", response_model=PropertyImageSchema, status_code=status.HTTP_200_OK)
async def get_by_id(id: str) -> PropertyImageSchema:
    """
    Response Model: PropertyImageSchema
    """
    # TODO: PropertyImage Not Found
    return await PropertyImageCRUD.get_by_id(id)


@router.get(
    "/filename/{filename}",
    response_model=List[PropertyImageSchema],
    status_code=status.HTTP_200_OK,
)
async def get_by_filename(filename: str) -> List[PropertyImageSchema]:
    """
    Response Model: List[PropertyImageSchema]
    """
    # TODO: PropertyImage Not Found
    return await PropertyImageCRUD.get_by_filename(filename)
