import pytest
from unittest.mock import Mock
from tech.domain.entities.users import User
from tech.interfaces.repositories.user_repository import UserRepository
from tech.use_cases.users.list_users_use_case import ListUsersUseCase


class TestListUsersUseCase:
    """Unit tests for the ListUsersUseCase."""

    def setup_method(self):
        """Set up test dependencies."""
        self.user_repository = Mock(spec=UserRepository)
        self.use_case = ListUsersUseCase(self.user_repository)

    def test_list_users_with_results(self):
        """Test listing users with results returned."""
        # Arrange
        limit = 10
        skip = 0
        mock_users = [Mock(spec=User) for _ in range(3)]
        self.user_repository.list_users.return_value = mock_users

        # Act
        result = self.use_case.execute(limit, skip)

        # Assert
        self.user_repository.list_users.assert_called_once_with(limit, skip)
        assert result == mock_users
        assert len(result) == 3

    def test_list_users_with_pagination(self):
        """Test listing users with pagination parameters."""
        # Arrange
        limit = 2
        skip = 5
        mock_users = [Mock(spec=User) for _ in range(2)]
        self.user_repository.list_users.return_value = mock_users

        # Act
        result = self.use_case.execute(limit, skip)

        # Assert
        self.user_repository.list_users.assert_called_once_with(limit, skip)
        assert result == mock_users
        assert len(result) == 2

    def test_list_users_with_empty_result(self):
        """Test listing users when no users are found."""
        # Arrange
        limit = 10
        skip = 0
        self.user_repository.list_users.return_value = []

        # Act
        result = self.use_case.execute(limit, skip)

        # Assert
        self.user_repository.list_users.assert_called_once_with(limit, skip)
        assert result == []
        assert len(result) == 0