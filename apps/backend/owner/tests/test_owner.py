import pytest
from bson import ObjectId
from faker import Faker

from ..src.crud.owner import OwnerCRUD
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
    ],
)
def test_create(test_app, monkeypatch, json_data, status_code):
    """
    Create Owner Unit Test
    Create Owner in DB collection owners
    """

    async def mock_create(_):
        """Monkeypatch"""
        date_time = fake.date_time()
        test_data = OwnerSchema.from_mongo(
            {
                "_id": ObjectId.from_datetime(date_time),
                "name": json_data["name"],
                "address": json_data["address"],
                "photo": json_data["photo"],
                "created": date_time,
                "updated": date_time,
            }
        )
        return test_data

    monkeypatch.setattr(OwnerCRUD, "create", mock_create)

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
