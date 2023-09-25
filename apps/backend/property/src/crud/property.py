from typing import List

from bson import ObjectId
from pymongo import ReturnDocument

from ..db.motor import Motor
from ..schemas.property import PropertyCreate, PropertySchema, PropertyUpdate


class PropertyCRUD:
    """
    Property CRUD operations using static methods
    """

    @classmethod
    async def create(cls, property: PropertyCreate) -> PropertySchema:
        """Create Property in DB collection properties
        :param property: PropertyCreate
        :return: PropertySchema
        """
        result = await Motor.db.properties.insert_one(property.to_mongo())
        if result.acknowledged:
            result = await Motor.db.properties.find_one({"_id": result.inserted_id})
            return PropertySchema.from_mongo(result)

        return None

    @classmethod
    async def update(cls, id: str, property: PropertyUpdate) -> PropertySchema:
        """Update Property in DB collection properties
        :param id: str Property ID
        :param property: PropertyUpdate
        :return: PropertySchema
        """
        result = await Motor.db.properties.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": property.to_mongo(exclude_none=True)},
            return_document=ReturnDocument.AFTER,
        )

        return PropertySchema.from_mongo(result)

    @classmethod
    async def delete(cls, id: str) -> bool:
        """Delete Property in DB collection properties
        :param id: str Property ID
        :return: bool
        """
        result = await Motor.db.properties.delete_one({"_id": ObjectId(id)})

        if result.deleted_count > 0:
            return True

        return False

    @classmethod
    async def get_all(cls) -> List[PropertySchema]:
        """Get all Properties in DB collection properties
        :return: List[PropertySchema]
        """
        result = []
        async for property in Motor.db.properties.find({}):
            result.append(PropertySchema.from_mongo(property))

        return result

    @classmethod
    async def get_by_id(cls, id: str) -> PropertySchema:
        """Get Property in DB collection properties by _id
        :param id: str Property ID
        :return: PropertySchema
        """
        result = await Motor.db.properties.find_one({"_id": ObjectId(id)})

        return PropertySchema.from_mongo(result)

    @classmethod
    async def get_by_name(cls, name: str) -> List[PropertySchema]:
        """Get Property in DB collection properties by name
        :param name: str Property name
        :return: List[PropertySchema]
        """
        result = []
        async for property in Motor.db.properties.find({"name": name}):
            result.append(PropertySchema.from_mongo(property))

        return result
