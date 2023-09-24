import pytest
import pytest_asyncio
from faker import Faker
from fastapi.testclient import TestClient

from ..src.config.settings import settings
from ..src.crud.owner import OwnerCRUD
from ..src.main import app
from ..src.schemas.owner import OwnerCreate, OwnerSchema

fake = Faker()
fake.seed_instance("million-and-up")


@pytest.fixture()
def test_app():
    """Single test app fixture"""
    settings.pytest_mode = True
    with TestClient(app) as test_client:
        yield test_client


@pytest_asyncio.fixture()
async def create_owner_fixture() -> OwnerSchema:
    """
    Create single owner fixture
    """
    created_at = fake.past_datetime()
    test_data = {
        "name": fake.name(),
        "address": fake.address(),
        "photo": fake.file_name(category="image"),
        "created": created_at,
        "updated": created_at,
    }

    new_owner = OwnerCreate(**test_data)

    result_owner = await OwnerCRUD.create(new_owner)

    assert result_owner.name == new_owner.name
    assert result_owner.address == new_owner.address
    assert result_owner.photo == new_owner.photo

    return result_owner
