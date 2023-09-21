from ..db.motor import Motor
from ..schemas.user import UserCreate, UserDB


class UserCRUD:
    """
    User CRUD opperations using static class methods
    """
    @classmethod
    async def get_by_username(cls, username: str) -> UserDB:
        """Get User in DB collection users
        :param username: str
        :return: UserDB
        """
        result = await Motor.db.users.find_one({"username": username})

        return UserDB.from_mongo(result)

    @classmethod
    async def create(cls, user: UserCreate) -> UserDB:
        """Create User in DB collection users
        :param user: UserCreate
        :return: UserDB
        """

        result = await Motor.db.users.insert_one(user.to_mongo())
        if result.acknowledged:
            result = await Motor.db.users.find_one({"_id": result.inserted_id})
            return UserDB.from_mongo(result)

        return None
