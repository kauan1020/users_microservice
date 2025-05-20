import pytest
from unittest.mock import Mock, patch
from tech.domain.entities.users import User
from tech.interfaces.schemas.user_schema import UserSchema
from tech.interfaces.repositories.user_repository import UserRepository
from tech.use_cases.users.update_user_use_case import UpdateUserUseCase


class TestUpdateUserUseCase:
    """Unit tests for the UpdateUserUseCase."""

    def setup_method(self):
        """Set up test dependencies."""
        self.user_repository = Mock(spec=UserRepository)
        self.use_case = UpdateUserUseCase(self.user_repository)
        self.user_data = UserSchema(
            username="updated_user",
            email="updated@example.com",
            password="NewPassword123",
            cpf="12345678901"
        )
        self.user_id = 1

    def test_successful_user_update(self):
        """Test successful update of a user when the user exists."""
        # Arrange
        mock_user = Mock(spec=User)
        self.user_repository.get_by_id.return_value = mock_user
        self.user_repository.update.return_value = mock_user

        # Act
        with patch("tech.use_cases.users.update_user_use_case.get_password_hash") as mock_get_hash:
            mock_get_hash.return_value = "new_hashed_password"
            result = self.use_case.execute(self.user_id, self.user_data)

        # Assert
        self.user_repository.get_by_id.assert_called_once_with(self.user_id)

        # Verify that user attributes were updated correctly
        assert mock_user.username == self.user_data.username
        assert mock_user.password == "new_hashed_password"
        assert mock_user.email == self.user_data.email
        assert mock_user.cpf == self.user_data.cpf

        self.user_repository.update.assert_called_once_with(mock_user)
        assert result == mock_user

    def test_update_nonexistent_user(self):
        """Test that updating a non-existent user raises a ValueError."""
        # Arrange
        self.user_repository.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.use_case.execute(self.user_id, self.user_data)

        assert "User not found" in str(exc_info.value)
        self.user_repository.get_by_id.assert_called_once_with(self.user_id)
        self.user_repository.update.assert_not_called()