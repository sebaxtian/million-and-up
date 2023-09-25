from typing import List

from bson import ObjectId
from pymongo import ReturnDocument

from ..db.motor import Motor
from ..schemas.property_trace import (
    PropertyTraceCreate,
    PropertyTraceSchema,
    PropertyTraceUpdate,
)


class PropertyTraceCRUD:
    """
    PropertyTrace CRUD operations using static methods
    """

    @classmethod
    async def create(cls, property_trace: PropertyTraceCreate) -> PropertyTraceSchema:
        """Create PropertyTrace in DB collection properties_trace
        :param property_trace: PropertyTraceCreate
        :return: PropertyTraceSchema
        """
        result = await Motor.db.properties_trace.insert_one(property_trace.to_mongo())
        if result.acknowledged:
            result = await Motor.db.properties_trace.find_one(
                {"_id": result.inserted_id}
            )
            return PropertyTraceSchema.from_mongo(result)

        return None

    @classmethod
    async def update(
        cls, id: str, property_trace: PropertyTraceUpdate
    ) -> PropertyTraceSchema:
        """Update PropertyTrace in DB collection properties_trace
        :param id: str PropertyTrace ID
        :param property_trace: PropertyTraceUpdate
        :return: PropertyTraceSchema
        """
        result = await Motor.db.properties_trace.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": property_trace.to_mongo(exclude_none=True)},
            return_document=ReturnDocument.AFTER,
        )

        return PropertyTraceSchema.from_mongo(result)

    @classmethod
    async def delete(cls, id: str) -> bool:
        """Delete PropertyTrace in DB collection properties_trace
        :param id: str PropertyTrace ID
        :return: bool
        """
        result = await Motor.db.properties_trace.delete_one({"_id": ObjectId(id)})

        if result.deleted_count > 0:
            return True

        return False

    @classmethod
    async def get_all(cls) -> List[PropertyTraceSchema]:
        """Get all Properties in DB collection properties_trace
        :return: List[PropertyTraceSchema]
        """
        result = []
        async for property_trace in Motor.db.properties_trace.find({}):
            result.append(PropertyTraceSchema.from_mongo(property_trace))

        return result

    @classmethod
    async def get_by_id(cls, id: str) -> PropertyTraceSchema:
        """Get PropertyTrace in DB collection properties_trace by _id
        :param id: str PropertyTrace ID
        :return: PropertyTraceSchema
        """
        result = await Motor.db.properties_trace.find_one({"_id": ObjectId(id)})

        return PropertyTraceSchema.from_mongo(result)

    @classmethod
    async def get_by_name(cls, name: str) -> List[PropertyTraceSchema]:
        """Get PropertyTrace in DB collection properties_trace by filename
        :param name: str PropertyTrace name
        :return: List[PropertyTraceSchema]
        """
        result = []
        async for property_trace in Motor.db.properties_trace.find({"name": name}):
            result.append(PropertyTraceSchema.from_mongo(property_trace))

        return result
