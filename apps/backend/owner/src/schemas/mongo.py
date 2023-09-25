from typing import Callable

from pydantic import BaseModel


class MongoBase(BaseModel):
    """
    Class that handles conversions between MongoDB '_id' key and our own 'id' key

    MongoDB uses `_id` as an internal default index key
    We can use that to our advantage
    """

    @classmethod
    def from_mongo(cls, data: dict) -> Callable:
        """Convert "_id" (str object) into "id" (UUID object)"""

        if not data:
            return data

        mongo_id = data.pop("_id", None)
        return cls(**dict(data, id=str(mongo_id)))

    def to_mongo(self, **kwargs) -> dict:
        """Convert "id" (UUID object) into "_id" (str object)"""

        # parsed = self.dict(**kwargs)
        parsed = self.model_dump(**kwargs)

        if "_id" not in parsed and "id" in parsed:
            parsed["_id"] = str(parsed.pop("id"))

        return parsed
