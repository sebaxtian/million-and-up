from typing import List

import pytest
import pytest_asyncio
from bson import ObjectId
from faker import Faker
from fastapi.testclient import TestClient

from ..src.config.settings import settings
from ..src.crud.property_trace import PropertyTraceCRUD
from ..src.main import app
from ..src.schemas.property_trace import PropertyTraceCreate, PropertyTraceSchema

fake = Faker()
fake.seed_instance("million-and-up")


@pytest.fixture()
def test_app():
    """Single test app fixture"""
    settings.pytest_mode = True
    with TestClient(app) as test_client:
        yield test_client


@pytest_asyncio.fixture()
async def create_property_trace_fixture() -> PropertyTraceSchema:
    """
    Create single property_trace fixture
    """
    created_at = fake.past_datetime()
    test_data = {
        "id_property": str(ObjectId()),
        "date_sale": str(fake.past_datetime()),
        "name": fake.company(),
        "value": fake.pyfloat(positive=True),
        "tax": fake.pyfloat(positive=True),
        "created": created_at,
        "updated": created_at,
    }

    new_property_trace = PropertyTraceCreate(**test_data)

    result_property_trace = await PropertyTraceCRUD.create(new_property_trace)

    assert result_property_trace.id_property == new_property_trace.id_property
    assert result_property_trace.date_sale == new_property_trace.date_sale
    assert result_property_trace.name == new_property_trace.name
    assert result_property_trace.value == new_property_trace.value
    assert result_property_trace.tax == new_property_trace.tax

    return result_property_trace


@pytest_asyncio.fixture()
async def create_properties_trace_fixture() -> List[PropertyTraceSchema]:
    """
    Create 5 properties_trace fixture
    """
    properties_trace = []
    for _ in range(0, 5):
        created_at = fake.past_datetime()
        new_property_trace = PropertyTraceCreate(
            **{
                "id_property": str(ObjectId()),
                "date_sale": str(fake.past_datetime()),
                "name": fake.company(),
                "value": fake.pyfloat(positive=True),
                "tax": fake.pyfloat(positive=True),
                "created": created_at,
                "updated": created_at,
            }
        )
        result_property_trace = await PropertyTraceCRUD.create(new_property_trace)
        properties_trace.append(result_property_trace)

    return properties_trace
