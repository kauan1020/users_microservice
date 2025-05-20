import pytest
from unittest.mock import Mock
from tech.domain.entities.users import User
from tech.interfaces.repositories.user_repository import UserRepository
from tech.use_cases.users.delete_user_use_case import DeleteUserUseCase


class TestDeleteUserUseCase:
    """Unit tests for the DeleteUserUseCase."""

    def setup_method(self):
        """Set up test dependencies."""
        self.user_repository = Mock(spec=UserRepository)
        self.use_case = DeleteUserUseCase(self.user_repository)

    def test_delete_existing_user(self):
        """Test successful deletion of an existing user."""
        # Arrange
        user_id = 1
        mock_user = Mock(spec=User)
        self.user_repository.get_by_id.return_value = mock_user

        # Act
        result = self.use_case.execute(user_id)

        # Assert
        self.user_repository.get_by_id.assert_called_once_with(user_id)
        self.user_repository.delete.assert_called_once_with(mock_user)
        assert result == {"message": "User deleted"}

    def test_delete_non_existent_user(self):
        """Test that trying to delete a non-existent user raises a ValueError."""
        # Arrange
        user_id = 999  # Non-existent ID
        self.user_repository.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.use_case.execute(user_id)

        assert "User not found" in str(exc_info.value)
        self.user_repository.get_by_id.assert_called_once_with(user_id)
        self.user_repository.delete.assert_not_called()