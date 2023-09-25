import random

import pytest
from bson import ObjectId
from faker import Faker
from fastapi import status

from ..src.schemas.property_image import PropertyImageBase, PropertyImageSchema

fake = Faker()
fake.seed_instance("million-and-up")


@pytest.mark.parametrize(
    "json_data, status_code",
    [
        [
            {
                "id_property": str(ObjectId()),
                "filename": fake.file_name(category="image"),
                "enabled": fake.pybool(),
            },
            status.HTTP_201_CREATED,
        ]
        # TODO: New test cases
    ],
)
def test_create(test_app, json_data, status_code):
    """
    Create PropertyImage Unit Test
    Create PropertyImage in DB collection property_images
    """

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    new_property_image = PropertyImageBase(**json_data)

    response = test_app.post(
        "/property_image/create", headers=headers, json=new_property_image.model_dump()
    )

    assert response.status_code == status_code
    property_image_created = PropertyImageSchema(**response.json())

    assert property_image_created.id_property == new_property_image.id_property
    assert property_image_created.filename == new_property_image.filename
    assert property_image_created.enabled == new_property_image.enabled


@pytest.mark.parametrize(
    "json_data, status_code",
    [
        [
            {
                "id_property": str(ObjectId()),
                "filename": fake.file_name(category="image"),
                "enabled": fake.pybool(),
            },
            status.HTTP_200_OK,
        ]
        # TODO: New test cases
    ],
)
def test_update(test_app, create_property_image_fixture, json_data, status_code):
    """
    Update PropertyImage Unit Test
    Update PropertyImage in DB collection property_images
    """

    # id single property_image fixture created
    id = create_property_image_fixture.id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    patch_property_image = PropertyImageBase(**json_data)

    response = test_app.put(
        f"/property_image/update/{id}",
        headers=headers,
        json=patch_property_image.model_dump(),
    )

    assert response.status_code == status_code
    property_image_updated = PropertyImageSchema(**response.json())

    assert property_image_updated.id_property == patch_property_image.id_property
    assert property_image_updated.filename == patch_property_image.filename
    assert property_image_updated.enabled == patch_property_image.enabled
    assert property_image_updated.created <= property_image_updated.updated


def test_delete(test_app, create_property_images_fixture):
    """
    Delete PropertyImage unit test
    Delete PropertyImage in DB collection property_images
    """

    # id from random property_image fixture list
    id = random.choice(create_property_images_fixture).id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.delete(f"/property_image/delete/{id}", headers=headers)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()


def test_get_all(test_app, create_property_images_fixture):
    """
    Get all PropertyImages unit test
    Get all PropertyImages in DB collection property_images
    """
    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.get("/property_image/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(create_property_images_fixture)


def test_get_by_id(test_app, create_property_images_fixture):
    """
    Get PropertyImage by id unit test
    Get PropertyImage by id in DB collection property_images
    """

    # random property_image from fixture list
    random_property_image: PropertyImageSchema = random.choice(
        create_property_images_fixture
    )
    # id from random property_image
    id = random_property_image.id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.get(f"/property_image/{id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    property_image = PropertyImageSchema(**response.json())

    assert property_image == random_property_image
    assert property_image.id == random_property_image.id


def test_get_by_filename(test_app, create_property_images_fixture):
    """
    Get PropertyImage by filename unit test
    Get PropertyImage by filename in DB collection property_images
    """

    # random property_image from fixture list
    random_property_image: PropertyImageSchema = random.choice(
        create_property_images_fixture
    )
    # filename from random property_image
    filename = random_property_image.filename

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.get(f"/property_image/filename/{filename}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    property_images = [
        PropertyImageSchema(**property_image) for property_image in response.json()
    ]

    for property_image in property_images:
        assert property_image.filename == random_property_image.filename
