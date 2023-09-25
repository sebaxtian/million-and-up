from fastapi import FastAPI

from .config.settings import settings
from .db.motor import Motor
from .routers import property_trace

app = FastAPI(version=settings.version, title=settings.name)

# Add created endpoints
app.include_router(property_trace.router)


@app.get("/")
async def root():
    return {
        "aboutme": "Welcome to Million and Up, Property Trace - RESTful API - Microservice",  # noqa: E501
        "docs": "/docs",
    }


@app.on_event("startup")
async def open_db_conn():
    """Initialize DB connection"""
    await Motor.connect()


@app.on_event("shutdown")
async def close_db_conn():
    """Close DB connection"""
    await Motor.close()
