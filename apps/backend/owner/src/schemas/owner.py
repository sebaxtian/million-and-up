from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import Field

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


class OwnerPatch(OwnerBase):
    """
    Patch Owner attributes
    """

    name: Optional[str] = None
    address: Optional[str] = None
    photo: Optional[str] = None


class OwnerUpdate(OwnerPatch):
    """Update Owner"""

    # WARNING! - Dont use:
    # updated: datetime = datetime.now(
    #                       tz=timezone(offset=-timedelta(hours=5),
    #                       name="America/Bogota"))
    # Use Field for default updated values
    updated: datetime = Field(
        default_factory=lambda: datetime.now(
            tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
        )
    )


class OwnerSchema(OwnerBase):
    """Owner Schema representation"""

    id: str
    created: datetime
    updated: datetime
