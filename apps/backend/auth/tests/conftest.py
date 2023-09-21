from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

from ..src.config.settings import settings
from ..src.crud.user import UserCRUD
from ..src.main import app
from ..src.schemas.user import UserDB


@pytest.fixture()
def test_app():
    """Single test app fixture"""
    settings.pytest_mode = True
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def userdb_fixture(monkeypatch):
    # Test data used as UserDB mock
    test_data = UserDB(
        id="507f1f77bcf86cd799439011",
        email="admin@example.com",
        username="admin",
        full_name="Admin User",
        hashed_password="$2b$12$K.vJmHzL8JhjPstI3rFf7uXSbiLfjr8Jr/mzhIIDRRtxyLFmffjl2",
        created=datetime.now(
            tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
        ),
        updated=datetime.now(
            tz=timezone(offset=-timedelta(hours=5), name="America/Bogota")
        ),
    )

    async def mock_create():
        """Monkeypatch"""
        return test_data

    async def mock_get_by_username(username: str = "admin"):
        """Monkeypatch"""
        return test_data

    # Mock crud methods using test_data
    monkeypatch.setattr(UserCRUD, "create", mock_create)
    monkeypatch.setattr(UserCRUD, "get_by_username", mock_get_by_username)
