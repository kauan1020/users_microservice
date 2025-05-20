import pytest
from unittest.mock import Mock
from datetime import datetime
from sqlalchemy.orm import Session
from tech.domain.entities.users import User


@pytest.fixture
def mock_session():
    """Fixture providing a mock SQLAlchemy session."""
    return Mock(spec=Session)


@pytest.fixture
def user_data():
    """Fixture providing common user data for tests."""
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "password": "hashed_password",
        "cpf": "12345678901",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }


@pytest.fixture
def test_user(user_data):
    """Fixture providing a User entity for tests."""
    return User(
        id=user_data["id"],
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"],
        cpf=user_data["cpf"]
    )


@pytest.fixture
def test_users():
    """Fixture providing a list of test User entities."""
    return [
        User(
            id=1,
            username="user1",
            email="user1@example.com",
            password="hash1",
            cpf="12345678901"
        ),
        User(
            id=2,
            username="user2",
            email="user2@example.com",
            password="hash2",
            cpf="98765432101"
        ),
        User(
            id=3,
            username="user3",
            email="user3@example.com",
            password="hash3",
            cpf="11122233344"
        )
    ]