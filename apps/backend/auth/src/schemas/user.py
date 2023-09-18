from datetime import datetime, timedelta, timezone

from mongo import MongoBase
from pydantic import UUID4


class UserBase(MongoBase):
    email: str
    name: str
    role: str


class UserCreate(UserBase):
    hashed_password: str
    created: datetime = datetime.now(
        tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
    )
    updated: datetime = created


class UserUpdate(UserBase):
    hashed_password: str
    updated: datetime = datetime.now(
        tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
    )


class UserSchema(UserBase):
    id: UUID4
    created: datetime
    updated: datetime
