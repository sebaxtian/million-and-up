import pytest
from faker import Faker

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
            201,
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
            200,
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
