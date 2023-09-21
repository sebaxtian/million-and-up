from datetime import datetime, timedelta, timezone

from .mongo import MongoBase


class OwnerBase(MongoBase):
    """Owner base model representation"""

    name: str
    address: str
    photo: str


class OwnerCreate(OwnerBase):
    """Create new Owner"""

    created: datetime = datetime.now(
        tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
    )
    updated: datetime = created


class OwnerUpdate(OwnerBase):
    """Update Owner"""

    updated: datetime = datetime.now(
        tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
    )


class OwnerSchema(OwnerBase):
    """Owner Schema representation"""

    id: str
    created: datetime
    updated: datetime
