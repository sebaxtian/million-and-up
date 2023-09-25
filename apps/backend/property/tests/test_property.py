import random

import pytest
from bson import ObjectId
from faker import Faker
from fastapi import status

from ..src.schemas.property import PropertyBase, PropertySchema

fake = Faker()
fake.seed_instance("million-and-up")


@pytest.mark.parametrize(
    "json_data, status_code",
    [
        [
            {
                "id_owner": str(ObjectId()),
                "name": fake.name(),
                "address": fake.address(),
                "price": fake.pyfloat(positive=True),
                "internal_code": fake.uuid4(),
                "year": fake.year(),
            },
            status.HTTP_201_CREATED,
        ]
        # TODO: New test cases
    ],
)
def test_create(test_app, json_data, status_code):
    """
    Create Property Unit Test
    Create Property in DB collection properties
    """

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    new_property = PropertyBase(**json_data)

    response = test_app.post(
        "/property/create", headers=headers, json=new_property.model_dump()
    )

    assert response.status_code == status_code
    property_created = PropertySchema(**response.json())

    assert property_created.id_owner == new_property.id_owner
    assert property_created.name == new_property.name
    assert property_created.address == new_property.address
    assert property_created.price == new_property.price
    assert property_created.internal_code == new_property.internal_code
    assert property_created.year == new_property.year


@pytest.mark.parametrize(
    "json_data, status_code",
    [
        [
            {
                "id_owner": str(ObjectId()),
                "name": fake.name(),
                "address": fake.address(),
                "price": fake.pyfloat(positive=True),
                "internal_code": fake.uuid4(),
                "year": fake.year(),
            },
            status.HTTP_200_OK,
        ]
        # TODO: New test cases
    ],
)
def test_update(test_app, create_property_fixture, json_data, status_code):
    """
    Update Property Unit Test
    Update Property in DB collection properties
    """

    # id single property fixture created
    id = create_property_fixture.id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    patch_property = PropertyBase(**json_data)

    response = test_app.put(
        f"/property/update/{id}", headers=headers, json=patch_property.model_dump()
    )

    assert response.status_code == status_code
    property_updated = PropertySchema(**response.json())

    assert property_updated.id_owner == patch_property.id_owner
    assert property_updated.name == patch_property.name
    assert property_updated.address == patch_property.address
    assert property_updated.price == patch_property.price
    assert property_updated.internal_code == patch_property.internal_code
    assert property_updated.year == patch_property.year
    assert property_updated.created <= property_updated.updated


def test_delete(test_app, create_properties_fixture):
    """
    Delete Property unit test
    Delete Property in DB collection properties
    """

    # id from random property fixture list
    id = random.choice(create_properties_fixture).id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.delete(f"/property/delete/{id}", headers=headers)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()


def test_get_all(test_app, create_properties_fixture):
    """
    Get all Owners unit test
    Get all Owners in DB collection properties
    """
    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.get("/property/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(create_properties_fixture)


def test_get_by_id(test_app, create_properties_fixture):
    """
    Get Property by id unit test
    Get Property by id in DB collection properties
    """

    # random property from fixture list
    random_property: PropertySchema = random.choice(create_properties_fixture)
    # id from random property
    id = random_property.id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.get(f"/property/{id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    property = PropertySchema(**response.json())

    assert property == random_property
    assert property.id == random_property.id


def test_get_by_name(test_app, create_properties_fixture):
    """
    Get Property by name unit test
    Get Property by name in DB collection properties
    """

    # random property from fixture list
    random_property: PropertySchema = random.choice(create_properties_fixture)
    # name from random property
    name = random_property.name

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.get(f"/property/name/{name}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    properties = [PropertySchema(**property) for property in response.json()]

    for property in properties:
        assert property.name == random_property.name
