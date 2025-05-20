import pytest
from unittest.mock import Mock
from tech.domain.entities.users import User
from tech.interfaces.repositories.user_repository import UserRepository
from tech.use_cases.users.get_user_by_cpf_use_case import GetUserByCpfUseCase


class TestGetUserByCpfUseCase:
    """Unit tests for the GetUserByCpfUseCase."""

    def setup_method(self):
        """Set up test dependencies."""
        self.user_repository = Mock(spec=UserRepository)
        self.use_case = GetUserByCpfUseCase(self.user_repository)
        self.cpf = "12345678901"

    def test_get_existing_user_by_cpf(self):
        """Test retrieving an existing user by CPF."""
        # Arrange
        mock_user = Mock(spec=User)
        self.user_repository.get_by_cpf.return_value = mock_user

        # Act
        result = self.use_case.execute(self.cpf)

        # Assert
        self.user_repository.get_by_cpf.assert_called_once_with(self.cpf)
        assert result == mock_user

    def test_get_nonexistent_user_by_cpf(self):
        """Test that trying to retrieve a non-existent user by CPF raises a ValueError."""
        # Arrange
        self.user_repository.get_by_cpf.return_value = None

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.use_case.execute(self.cpf)

        assert "User not found" in str(exc_info.value)
        self.user_repository.get_by_cpf.assert_called_once_with(self.cpf)
