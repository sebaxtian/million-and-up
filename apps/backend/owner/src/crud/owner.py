from typing import List

from pymongo import ReturnDocument

from ..db.motor import Motor
from ..schemas.owner import OwnerCreate, OwnerSchema, OwnerUpdate


class OwnerCRUD:
    """
    Owner CRUD operations using static methods
    """

    @classmethod
    async def create(cls, owner: OwnerCreate) -> OwnerSchema:
        """Create Owner in DB collection owners
        :param owner: OwnerCreate
        :return: OwnerSchema
        """
        result = await Motor.db.owners.insert_one(owner.to_mongo())
        if result.acknowledged:
            result = await Motor.db.owners.find_one({"_id": result.inserted_id})
            return OwnerSchema.from_mongo(result)

        return None

    @classmethod
    async def update(cls, id: str, owner: OwnerUpdate) -> OwnerSchema:
        """Update Owner in DB collection owners
        :param id: str Owner ID
        :param owner: OwnerUpdate
        :return: OwnerSchema
        """
        result = await Motor.db.owners.find_one_and_update(
            {"_id": id},
            {"$set": owner.to_mongo()},
            return_document=ReturnDocument.AFTER,
        )

        return result

    @classmethod
    async def delete(cls, id: str) -> bool:
        """Delete Owner in DB collection owners
        :param id: str Owner ID
        :return: bool
        """
        result = await Motor.db.owners.delete_one({"_id": id})

        if result.deleted_count > 0:
            return True

        return False

    @classmethod
    async def get_all(cls) -> List[OwnerSchema]:
        """Get all Owners in DB collection owners
        :return: List[OwnerSchema]
        """
        result = []
        async for owner in Motor.db.owners.find({}):
            result.append(OwnerSchema.from_mongo(owner))

        return result

    @classmethod
    async def get_by_id(cls, id: str) -> OwnerSchema:
        """Get Owner in DB collection owners by _id
        :param id: str Owner ID
        :return: OwnerSchema
        """
        result = await Motor.db.owners.find_one({"_id": id})

        return OwnerSchema.from_mongo(result)

    @classmethod
    async def get_by_name(cls, name: str) -> List[OwnerSchema]:
        """Get Owner in DB collection owners by name
        :param name: str Owner name
        :return: List[OwnerSchema]
        """
        result = []
        async for owner in Motor.db.owners.find({"name": name}):
            result.append(OwnerSchema.from_mongo(owner))

        return result
