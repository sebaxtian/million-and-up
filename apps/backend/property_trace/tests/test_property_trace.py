import random

import pytest
from bson import ObjectId
from faker import Faker
from fastapi import status

from ..src.schemas.property_trace import PropertyTraceBase, PropertyTraceSchema

fake = Faker()
fake.seed_instance("million-and-up")


@pytest.mark.parametrize(
    "json_data, status_code",
    [
        [
            {
                "id_property": str(ObjectId()),
                "date_sale": str(fake.past_datetime()),
                "name": fake.company(),
                "value": fake.pyfloat(positive=True),
                "tax": fake.pyfloat(positive=True),
            },
            status.HTTP_201_CREATED,
        ]
        # TODO: New test cases
    ],
)
def test_create(test_app, json_data, status_code):
    """
    Create PropertyTrace Unit Test
    Create PropertyTrace in DB collection properties_trace
    """

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    new_property_trace = PropertyTraceBase(**json_data)

    response = test_app.post(
        "/property_trace/create",
        headers=headers,
        json=new_property_trace.model_dump(),
    )

    assert response.status_code == status_code
    property_trace_created = PropertyTraceSchema(**response.json())

    assert property_trace_created.id_property == new_property_trace.id_property
    assert property_trace_created.date_sale == new_property_trace.date_sale
    assert property_trace_created.name == new_property_trace.name
    assert property_trace_created.value == new_property_trace.value
    assert property_trace_created.tax == new_property_trace.tax


@pytest.mark.parametrize(
    "json_data, status_code",
    [
        [
            {
                "id_property": str(ObjectId()),
                "date_sale": str(fake.past_datetime()),
                "name": fake.company(),
                "value": fake.pyfloat(),
                "tax": fake.pyfloat(),
            },
            status.HTTP_200_OK,
        ]
        # TODO: New test cases
    ],
)
def test_update(test_app, create_property_trace_fixture, json_data, status_code):
    """
    Update PropertyTrace Unit Test
    Update PropertyTrace in DB collection properties_trace
    """

    # id single property_trace fixture created
    id = create_property_trace_fixture.id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    patch_property_trace = PropertyTraceBase(**json_data)

    response = test_app.put(
        f"/property_trace/update/{id}",
        headers=headers,
        json=patch_property_trace.model_dump(),
    )

    assert response.status_code == status_code
    property_trace_updated = PropertyTraceSchema(**response.json())

    assert property_trace_updated.id_property == patch_property_trace.id_property
    assert property_trace_updated.date_sale == patch_property_trace.date_sale
    assert property_trace_updated.name == patch_property_trace.name
    assert property_trace_updated.value == patch_property_trace.value
    assert property_trace_updated.tax == patch_property_trace.tax
    assert property_trace_updated.created <= property_trace_updated.updated


def test_delete(test_app, create_properties_trace_fixture):
    """
    Delete PropertyTrace unit test
    Delete PropertyTrace in DB collection properties_trace
    """

    # id from random property_trace fixture list
    id = random.choice(create_properties_trace_fixture).id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.delete(f"/property_trace/delete/{id}", headers=headers)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()


def test_get_all(test_app, create_properties_trace_fixture):
    """
    Get all PropertyTrace unit test
    Get all PropertyTrace in DB collection properties_trace
    """
    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.get("/property_trace/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(create_properties_trace_fixture)


def test_get_by_id(test_app, create_properties_trace_fixture):
    """
    Get PropertyTrace by id unit test
    Get PropertyTrace by id in DB collection properties_trace
    """

    # random property_trace from fixture list
    random_property_trace: PropertyTraceSchema = random.choice(
        create_properties_trace_fixture
    )
    # id from random property_trace
    id = random_property_trace.id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.get(f"/property_trace/{id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    property_trace = PropertyTraceSchema(**response.json())

    assert property_trace == random_property_trace
    assert property_trace.id == random_property_trace.id


def test_get_by_name(test_app, create_properties_trace_fixture):
    """
    Get PropertyTrace by name unit test
    Get PropertyTrace by name in DB collection properties_trace
    """

    # random property_trace from fixture list
    random_property_trace: PropertyTraceSchema = random.choice(
        create_properties_trace_fixture
    )
    # name from random property_trace
    name = random_property_trace.name

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.get(f"/property_trace/name/{name}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    property_images = [
        PropertyTraceSchema(**property_trace) for property_trace in response.json()
    ]

    for property_trace in property_images:
        assert property_trace.name == random_property_trace.name
