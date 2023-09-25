from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import Field

from .mongo import MongoBase


class PropertyImageBase(MongoBase):
    """PropertyImage base model representation"""

    id_property: str
    filename: str
    enabled: bool = True


class PropertyImageCreate(PropertyImageBase):
    """Create new PropertyImage"""

    created: datetime = datetime.now(
        tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
    )
    updated: datetime = created


class PropertyImagePatch(PropertyImageBase):
    """
    Patch PropertyImage attributes
    """

    id_property: Optional[str] = None
    filename: Optional[str] = None
    enabled: Optional[bool] = None


class PropertyImageUpdate(PropertyImagePatch):
    """Update PropertyImage"""

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


class PropertyImageSchema(PropertyImageBase):
    """PropertyImage Schema representation"""

    id: str
    created: datetime
    updated: datetime
