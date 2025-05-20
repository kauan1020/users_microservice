# tests/unit/use_cases/gateways/test_user_gateway.py
import pytest
from unittest.mock import Mock, patch
from tech.domain.entities.users import User
from tech.interfaces.gateways.user_gateway import UserGateway
from tech.infra.repositories.sql_alchemy_user_repository import SQLAlchemyUserRepository


class TestUserGateway:
    """Unit tests for the UserGateway."""

    def setup_method(self):
        """Set up test dependencies."""
        self.mock_session = Mock()

        # Create a patch for the SQLAlchemyUserRepository
        self.repository_patch = patch('tech.interfaces.gateways.user_gateway.SQLAlchemyUserRepository')
        self.mock_repository_class = self.repository_patch.start()

        # Configure the mock to return a mock repository instance
        self.mock_repository = Mock()
        self.mock_repository_class.return_value = self.mock_repository

        # Initialize the gateway with the mock session
        self.gateway = UserGateway(self.mock_session)

    def teardown_method(self):
        """Clean up after tests."""
        self.repository_patch.stop()

    def test_add_user(self):
        """Test that add method delegates to repository."""
        # Arrange
        # Create a real User instance instead of a Mock to avoid __dict__ issues
        mock_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            cpf="12345678901"
        )
        self.mock_repository.add.return_value = mock_user

        # Act
        result = self.gateway.add(mock_user)

        # Assert
        self.mock_repository.add.assert_called_once_with(mock_user)
        assert result == mock_user

    def test_get_by_id(self):
        """Test that get_by_id method delegates to repository."""
        # Arrange
        user_id = 1
        mock_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            cpf="12345678901"
        )
        self.mock_repository.get_by_id.return_value = mock_user

        # Act
        result = self.gateway.get_by_id(user_id)

        # Assert
        self.mock_repository.get_by_id.assert_called_once_with(user_id)
        assert result == mock_user

    def test_get_by_cpf(self):
        """Test that get_by_cpf method delegates to repository."""
        # Arrange
        cpf = "12345678901"
        mock_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            cpf=cpf
        )
        self.mock_repository.get_by_cpf.return_value = mock_user

        # Act
        result = self.gateway.get_by_cpf(cpf)

        # Assert
        self.mock_repository.get_by_cpf.assert_called_once_with(cpf)
        assert result == mock_user

    def test_get_by_username_or_email_or_cpf(self):
        """Test that get_by_username_or_email_or_cpf method delegates to repository."""
        # Arrange
        username = "testuser"
        email = "test@example.com"
        cpf = "12345678901"
        mock_user = User(
            id=1,
            username=username,
            email=email,
            password="hashed_password",
            cpf=cpf
        )
        self.mock_repository.get_by_username_or_email_or_cpf.return_value = mock_user

        # Act
        result = self.gateway.get_by_username_or_email_or_cpf(username, email, cpf)

        # Assert
        self.mock_repository.get_by_username_or_email_or_cpf.assert_called_once_with(username, email, cpf)
        assert result == mock_user

    def test_list_users(self):
        """Test that list_users method delegates to repository."""
        # Arrange
        limit = 10
        skip = 0
        mock_users = [
            User(id=1, username="user1", email="user1@example.com", password="hash1", cpf="12345678901"),
            User(id=2, username="user2", email="user2@example.com", password="hash2", cpf="98765432101")
        ]
        self.mock_repository.list_users.return_value = mock_users

        # Act
        result = self.gateway.list_users(limit, skip)

        # Assert
        self.mock_repository.list_users.assert_called_once_with(limit, skip)
        assert result == mock_users
        assert len(result) == 2

    def test_update(self):
        """Test that update method delegates to repository."""
        # Arrange
        mock_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            cpf="12345678901"
        )
        self.mock_repository.update.return_value = mock_user

        # Act
        result = self.gateway.update(mock_user)

        # Assert
        self.mock_repository.update.assert_called_once_with(mock_user)
        assert result == mock_user

    def test_delete(self):
        """Test that delete method delegates to repository."""
        # Arrange
        mock_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            cpf="12345678901"
        )

        # Act
        self.gateway.delete(mock_user)

        # Assert
        self.mock_repository.delete.assert_called_once_with(mock_user)