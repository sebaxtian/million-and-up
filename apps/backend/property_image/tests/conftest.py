from typing import List

import pytest
import pytest_asyncio
from bson import ObjectId
from faker import Faker
from fastapi.testclient import TestClient

from ..src.config.settings import settings
from ..src.crud.property_image import PropertyImageCRUD
from ..src.main import app
from ..src.schemas.property_image import PropertyImageCreate, PropertyImageSchema

fake = Faker()
fake.seed_instance("million-and-up")


@pytest.fixture()
def test_app():
    """Single test app fixture"""
    settings.pytest_mode = True
    with TestClient(app) as test_client:
        yield test_client


@pytest_asyncio.fixture()
async def create_property_image_fixture() -> PropertyImageSchema:
    """
    Create single property_image fixture
    """
    created_at = fake.past_datetime()
    test_data = {
        "id_property": str(ObjectId()),
        "filename": fake.file_name(category="image"),
        "enabled": fake.pybool(),
        "created": created_at,
        "updated": created_at,
    }

    new_property_image = PropertyImageCreate(**test_data)

    result_property_image = await PropertyImageCRUD.create(new_property_image)

    assert result_property_image.id_property == new_property_image.id_property
    assert result_property_image.filename == new_property_image.filename
    assert result_property_image.enabled == new_property_image.enabled

    return result_property_image


@pytest_asyncio.fixture()
async def create_property_images_fixture() -> List[PropertyImageSchema]:
    """
    Create 5 property_images fixture
    """
    property_images = []
    for _ in range(0, 5):
        created_at = fake.past_datetime()
        new_property_image = PropertyImageCreate(
            **{
                "id_property": str(ObjectId()),
                "filename": fake.file_name(category="image"),
                "enabled": fake.pybool(),
                "created": created_at,
                "updated": created_at,
            }
        )
        result_property_image = await PropertyImageCRUD.create(new_property_image)
        property_images.append(result_property_image)

    return property_images
