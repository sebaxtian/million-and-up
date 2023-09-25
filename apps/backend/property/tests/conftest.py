from typing import List

import pytest
import pytest_asyncio
from bson import ObjectId
from faker import Faker
from fastapi.testclient import TestClient

from ..src.config.settings import settings
from ..src.crud.property import PropertyCRUD
from ..src.main import app
from ..src.schemas.property import PropertyCreate, PropertySchema

fake = Faker()
fake.seed_instance("million-and-up")


@pytest.fixture()
def test_app():
    """Single test app fixture"""
    settings.pytest_mode = True
    with TestClient(app) as test_client:
        yield test_client


@pytest_asyncio.fixture()
async def create_property_fixture() -> PropertySchema:
    """
    Create single property fixture
    """
    created_at = fake.past_datetime()
    test_data = {
        "id_owner": str(ObjectId()),
        "name": fake.name(),
        "address": fake.address(),
        "price": fake.pyfloat(positive=True),
        "internal_code": fake.uuid4(),
        "year": fake.year(),
        "created": created_at,
        "updated": created_at,
    }

    new_property = PropertyCreate(**test_data)

    result_property = await PropertyCRUD.create(new_property)

    assert result_property.id_owner == new_property.id_owner
    assert result_property.name == new_property.name
    assert result_property.address == new_property.address
    assert result_property.price == new_property.price
    assert result_property.internal_code == new_property.internal_code
    assert result_property.year == new_property.year

    return result_property


@pytest_asyncio.fixture()
async def create_properties_fixture() -> List[PropertySchema]:
    """
    Create 5 properties fixture
    """
    properties = []
    for _ in range(0, 5):
        created_at = fake.past_datetime()
        new_property = PropertyCreate(
            **{
                "id_owner": str(ObjectId()),
                "name": fake.name(),
                "address": fake.address(),
                "price": fake.pyfloat(positive=True),
                "internal_code": fake.uuid4(),
                "year": fake.year(),
                "created": created_at,
                "updated": created_at,
            }
        )
        result_property = await PropertyCRUD.create(new_property)
        properties.append(result_property)

    return properties
