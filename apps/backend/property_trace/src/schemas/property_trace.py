from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import Field

from .mongo import MongoBase


class PropertyTraceBase(MongoBase):
    """PropertyTrace base model representation"""

    id_property: str
    date_sale: str
    name: str
    value: float
    tax: float


class PropertyTraceCreate(PropertyTraceBase):
    """Create new PropertyTrace"""

    created: datetime = datetime.now(
        tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
    )
    updated: datetime = created


class PropertyTracePatch(PropertyTraceBase):
    """
    Patch PropertyTrace attributes
    """

    id_property: Optional[str] = None
    date_sale: Optional[str] = None
    name: Optional[str] = None
    value: Optional[float] = None
    tax: Optional[float] = None


class PropertyTraceUpdate(PropertyTracePatch):
    """Update PropertyTrace"""

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


class PropertyTraceSchema(PropertyTraceBase):
    """PropertyTrace Schema representation"""

    id: str
    created: datetime
    updated: datetime
