from fastapi import FastAPI

from .config.settings import settings

app = FastAPI(version=settings.version, title=settings.name)
