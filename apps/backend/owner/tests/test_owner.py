import random

import pytest
from faker import Faker
from fastapi import status

from ..src.schemas.owner import OwnerBase, OwnerSchema

fake = Faker()
fake.seed_instance("million-and-up")


@pytest.mark.parametrize(
    "json_data, status_code",
    [
        [
            {
                "name": fake.name(),
                "address": fake.address(),
                "photo": fake.file_name(category="image"),
            },
            status.HTTP_201_CREATED,
        ]
        # TODO: New test cases
    ],
)
def test_create(test_app, json_data, status_code):
    """
    Create Owner Unit Test
    Create Owner in DB collection owners
    """

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    new_owner = OwnerBase(**json_data)

    response = test_app.post(
        "/owner/create", headers=headers, json=new_owner.model_dump()
    )

    assert response.status_code == status_code
    owner_created = OwnerSchema(**response.json())
    assert owner_created.name == new_owner.name
    assert owner_created.address == new_owner.address
    assert owner_created.photo == new_owner.photo


@pytest.mark.parametrize(
    "json_data, status_code",
    [
        [
            {
                "name": fake.name(),
                "address": fake.address(),
                "photo": fake.file_name(category="image"),
            },
            status.HTTP_200_OK,
        ]
        # TODO: New test cases
    ],
)
def test_update(test_app, create_owner_fixture, json_data, status_code):
    """
    Update Owner Unit Test
    Update Owner in DB collection owners
    """

    # id single owner fixture created
    id = create_owner_fixture.id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    patch_owner = OwnerBase(**json_data)

    response = test_app.put(
        f"/owner/update/{id}", headers=headers, json=patch_owner.model_dump()
    )

    assert response.status_code == status_code
    owner_updated = OwnerSchema(**response.json())

    assert owner_updated.name == patch_owner.name
    assert owner_updated.address == patch_owner.address
    assert owner_updated.photo == patch_owner.photo
    assert owner_updated.created <= owner_updated.updated


def test_delete(test_app, create_owners_fixture):
    """
    Delete Owner unit test
    Delete Owner in DB collection owners
    """

    # id from random owner fixture list
    id = random.choice(create_owners_fixture).id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.delete(f"/owner/delete/{id}", headers=headers)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.json()


def test_get_all(test_app, create_owners_fixture):
    """
    Get all Owners unit test
    Get all Owners in DB collection owners
    """
    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.get("/owner/", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(create_owners_fixture)


def test_get_by_id(test_app, create_owners_fixture):
    """
    Get Owner by id unit test
    Get Owner by id in DB collection owners
    """

    # random owner from fixture list
    random_owner: OwnerSchema = random.choice(create_owners_fixture)
    # id from random owner
    id = random_owner.id

    # HTTP headers
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "token": "test",
    }

    response = test_app.get(f"/owner/{id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    owner = OwnerSchema(**response.json())

    assert owner == random_owner
    assert owner.id == random_owner.id
