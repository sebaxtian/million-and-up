from mongomock_motor import AsyncMongoMockClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from ..config.settings import settings


class Motor:
    """MongoDD database async engine class

    conn: AsyncIOMotorClient instance
    db: AsyncIOMotorDatabase instance
    """

    conn: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    @classmethod
    async def connect(cls, timeout=5000):
        """Initialize Connection to MongoDB
        Setting server connection timeout to 5 (default is 30) seconds

        conn: initialize AsyncIOMotorClient instance
        db: initialize AsyncIOMotorDatabase instance
        """

        # Pytest Mode
        if settings.pytest_mode:
            cls.conn = AsyncMongoMockClient()
        else:
            cls.conn = AsyncIOMotorClient(
                settings.mongodb_url, serverSelectionTimeoutMS=timeout
            )
        cls.db = cls.conn.million

    @classmethod
    async def close(cls):
        """Close MongoDB Connection"""

        cls.conn.close()
