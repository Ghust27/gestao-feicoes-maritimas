import hashlib
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from src.domain.entities.user import User
from src.schemas.user import Role, UserDTO

raw_test_password = "1234567890"
hash_object = hashlib.sha256(raw_test_password.encode("utf-8"))
hash_hex = hash_object.hexdigest()


@pytest.fixture
def base_user():
    return UserDTO(
        name="Andre",
        email="teste@teste.com.br",
        hashed_password=hash_hex,
        role=Role.OPERATOR,
    )

def test_generation_of_uuid_and_creation_date(base_user):
    user = User(base_user)
    assert user.id is not None
    assert user.created_at is not None


def test_user_must_respect_provided_id_and_date_of_creation(base_user):
    expected_id = uuid4()
    expected_user_creation_date = datetime(2026,1,2,tzinfo=timezone.utc)

    user = User(
        base_user,
        id=expected_id,
        created_at=expected_user_creation_date
    )
    
    assert user.id == expected_id
    assert user.created_at == expected_user_creation_date

def test_cannot_delete_user_with_assigned_oil_feature(base_user):
    user = User(base_user)
    with pytest.raises(ValueError) as err:
        user.validate_delete(2) 
    assert str(err.value) == "Cannot delete a user with confirmed features."