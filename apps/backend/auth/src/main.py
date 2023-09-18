from fastapi import FastAPI

from .config.settings import settings
from .db.motor import Motor

app = FastAPI(version=settings.version, title=settings.name)


@app.on_event("startup")
async def open_db_conn():
    """Initialize DB connection"""

    await Motor.connect()


@app.on_event("shutdown")
async def close_db_conn():
    """Close DB connection"""

    await Motor.close()
