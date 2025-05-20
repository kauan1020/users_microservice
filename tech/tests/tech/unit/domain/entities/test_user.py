# tests/unit/domain/entities/test_user.py
import pytest
from datetime import datetime, timedelta
from tech.domain.entities.users import User


class TestUser:
    """Unit tests for the User entity."""

    def setup_method(self):
        """Set up test fixtures."""
        self.user = User(
            id=1,
            username="testuser",
            password="hashed_password",
            cpf="12345678901",
            email="test@example.com"
        )

    def test_initialization(self):
        """Test that a User is correctly initialized with all attributes."""
        assert self.user.id == 1
        assert self.user.username == "testuser"
        assert self.user.password == "hashed_password"
        assert self.user.cpf == "12345678901"
        assert self.user.email == "test@example.com"
        assert isinstance(self.user.created_at, datetime)
        assert isinstance(self.user.updated_at, datetime)

    def test_update_password(self):
        """Test that update_password changes the password and updates the updated_at timestamp."""
        # Store the original updated_at timestamp
        original_updated_at = self.user.updated_at

        # Allow some time to pass to ensure timestamps are different
        import time
        time.sleep(0.001)

        # Update the password
        new_password = "new_hashed_password"
        self.user.update_password(new_password)

        # Verify that the password was updated
        assert self.user.password == new_password

        # Verify that the updated_at timestamp was updated
        assert self.user.updated_at > original_updated_at

    def test_update_email(self):
        """Test that update_email changes the email and updates the updated_at timestamp."""
        # Store the original updated_at timestamp
        original_updated_at = self.user.updated_at

        # Allow some time to pass to ensure timestamps are different
        import time
        time.sleep(0.001)

        # Update the email
        new_email = "new_email@example.com"
        self.user.update_email(new_email)

        # Verify that the email was updated
        assert self.user.email == new_email

        # Verify that the updated_at timestamp was updated
        assert self.user.updated_at > original_updated_at

    def test_created_at_initialized(self):
        """Test that created_at is initialized to the current time."""
        # The created_at timestamp should be recent (within the last second)
        time_difference = datetime.now() - self.user.created_at
        assert time_difference < timedelta(seconds=1)

    def test_creation_without_id(self):
        """Test that a User can be created without an ID."""
        user = User(
            username="nouser",
            password="password",
            cpf="98765432101",
            email="no@example.com"
        )

        assert user.id is None
        assert user.username == "nouser"
        assert user.password == "password"
        assert user.cpf == "98765432101"
        assert user.email == "no@example.com"