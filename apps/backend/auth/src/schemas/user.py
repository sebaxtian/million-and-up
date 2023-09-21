from datetime import datetime, timedelta, timezone

from .mongo import MongoBase


class UserBase(MongoBase):
    """User base model representation"""

    email: str
    username: str
    full_name: str
    role: str = "admin"
    disabled: bool = False


class UserCreate(UserBase):
    """Create new User with hashed password"""

    hashed_password: str
    created: datetime = datetime.now(
        tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
    )
    updated: datetime = created


class UserUpdate(UserBase):
    """Update User with hashed password"""

    hashed_password: str
    updated: datetime = datetime.now(
        tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
    )


class UserDB(UserBase):
    """User DB representation"""

    id: str
    hashed_password: str
    created: datetime
    updated: datetime


class UserSchema(UserBase):
    """User Schema representation"""

    id: str
    created: datetime
    updated: datetime
