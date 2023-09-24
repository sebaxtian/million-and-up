import pytest
from fastapi.testclient import TestClient

from ..src.config.settings import settings
from ..src.main import app


@pytest.fixture()
def test_app():
    """Single test app fixture"""
    settings.pytest_mode = True
    with TestClient(app) as test_client:
        yield test_client
