# tests/unit/interfaces/presenters/test_user_presenter.py
import pytest
from unittest.mock import Mock
from tech.domain.entities.users import User
from tech.interfaces.presenters.user_presenter import UserPresenter


class TestUserPresenter:
    """Unit tests for the UserPresenter."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create a mock user with all necessary attributes
        self.mock_user = Mock(spec=User)
        self.mock_user.id = 1
        self.mock_user.username = "testuser"
        self.mock_user.email = "test@example.com"
        self.mock_user.password = "hashed_password"  # Should not be included in presentation
        self.mock_user.cpf = "12345678901"  # Included in the presentation based on actual implementation

    def test_present_user(self):
        """Test that present_user returns the correct format with password excluded."""
        # Act
        result = UserPresenter.present_user(self.mock_user)

        # Assert
        assert isinstance(result, dict)
        assert result["id"] == 1
        assert result["username"] == "testuser"
        assert result["email"] == "test@example.com"
        assert result["cpf"] == "12345678901"  # CPF is included in the actual implementation
        assert "password" not in result  # Only password is excluded

    def test_present_user_list(self):
        """Test that present_user_list formats a list of users correctly."""
        # Arrange
        mock_user2 = Mock(spec=User)
        mock_user2.id = 2
        mock_user2.username = "user2"
        mock_user2.email = "user2@example.com"
        mock_user2.password = "hash2"
        mock_user2.cpf = "98765432101"

        mock_users = [self.mock_user, mock_user2]

        # Act
        result = UserPresenter.present_user_list(mock_users)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2

        assert result[0]["id"] == 1
        assert result[0]["username"] == "testuser"
        assert result[0]["email"] == "test@example.com"
        assert result[0]["cpf"] == "12345678901"  # CPF is included
        assert "password" not in result[0]  # Only password is excluded

        assert result[1]["id"] == 2
        assert result[1]["username"] == "user2"
        assert result[1]["email"] == "user2@example.com"
        assert result[1]["cpf"] == "98765432101"  # CPF is included
        assert "password" not in result[1]  # Only password is excluded

    def test_present_empty_user_list(self):
        """Test that present_user_list handles an empty list correctly."""
        # Act
        result = UserPresenter.present_user_list([])

        # Assert
        assert isinstance(result, list)
        assert len(result) == 0