from typing import List

from bson import ObjectId
from pymongo import ReturnDocument

from ..db.motor import Motor
from ..schemas.property_image import (
    PropertyImageCreate,
    PropertyImageSchema,
    PropertyImageUpdate,
)


class PropertyImageCRUD:
    """
    PropertyImage CRUD operations using static methods
    """

    @classmethod
    async def create(cls, property_image: PropertyImageCreate) -> PropertyImageSchema:
        """Create PropertyImage in DB collection property_images
        :param property_image: PropertyImageCreate
        :return: PropertyImageSchema
        """
        result = await Motor.db.property_images.insert_one(property_image.to_mongo())
        if result.acknowledged:
            result = await Motor.db.property_images.find_one(
                {"_id": result.inserted_id}
            )
            return PropertyImageSchema.from_mongo(result)

        return None

    @classmethod
    async def update(
        cls, id: str, property_image: PropertyImageUpdate
    ) -> PropertyImageSchema:
        """Update PropertyImage in DB collection property_images
        :param id: str PropertyImage ID
        :param property_image: PropertyImageUpdate
        :return: PropertyImageSchema
        """
        result = await Motor.db.property_images.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": property_image.to_mongo(exclude_none=True)},
            return_document=ReturnDocument.AFTER,
        )

        return PropertyImageSchema.from_mongo(result)

    @classmethod
    async def delete(cls, id: str) -> bool:
        """Delete PropertyImage in DB collection property_images
        :param id: str PropertyImage ID
        :return: bool
        """
        result = await Motor.db.property_images.delete_one({"_id": ObjectId(id)})

        if result.deleted_count > 0:
            return True

        return False

    @classmethod
    async def get_all(cls) -> List[PropertyImageSchema]:
        """Get all Properties in DB collection property_images
        :return: List[PropertyImageSchema]
        """
        result = []
        async for property_image in Motor.db.property_images.find({}):
            result.append(PropertyImageSchema.from_mongo(property_image))

        return result

    @classmethod
    async def get_by_id(cls, id: str) -> PropertyImageSchema:
        """Get PropertyImage in DB collection property_images by _id
        :param id: str PropertyImage ID
        :return: PropertyImageSchema
        """
        result = await Motor.db.property_images.find_one({"_id": ObjectId(id)})

        return PropertyImageSchema.from_mongo(result)

    @classmethod
    async def get_by_filename(cls, filename: str) -> List[PropertyImageSchema]:
        """Get PropertyImage in DB collection property_images by filename
        :param filename: str PropertyImage filename
        :return: List[PropertyImageSchema]
        """
        result = []
        async for property_image in Motor.db.property_images.find(
            {"filename": filename}
        ):
            result.append(PropertyImageSchema.from_mongo(property_image))

        return result
