from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import Field

from .mongo import MongoBase


class PropertyBase(MongoBase):
    """Property base model representation"""

    id_owner: str
    name: str
    address: str
    price: float
    internal_code: str
    year: int


class PropertyCreate(PropertyBase):
    """Create new Property"""

    created: datetime = datetime.now(
        tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
    )
    updated: datetime = created


class PropertyPatch(PropertyBase):
    """
    Patch Property attributes
    """

    id_owner: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    price: Optional[float] = None
    internal_code: Optional[str] = None
    year: Optional[int] = None


class PropertyUpdate(PropertyPatch):
    """Update Property"""

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


class PropertySchema(PropertyBase):
    """Property Schema representation"""

    id: str
    created: datetime
    updated: datetime
