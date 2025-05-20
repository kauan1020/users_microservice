import pytest
from unittest.mock import Mock, patch
from tech.domain.entities.users import User
from tech.interfaces.schemas.user_schema import UserSchema
from tech.interfaces.repositories.user_repository import UserRepository
from tech.use_cases.users.create_user_use_case import CreateUserUseCase


class TestCreateUserUseCase:
    """Unit tests for the CreateUserUseCase."""

    def setup_method(self):
        """Set up test dependencies."""
        self.user_repository = Mock(spec=UserRepository)
        self.use_case = CreateUserUseCase(self.user_repository)
        self.user_data = UserSchema(
            username="testuser",
            email="test@example.com",
            password="Password123",
            cpf="12345678901"
        )

    def test_successful_user_creation(self):
        """Test successful user creation when all conditions are met."""
        # Arrange
        self.user_repository.get_by_username_or_email_or_cpf.return_value = None

        # Mock the get_password_hash function
        with patch("tech.use_cases.users.create_user_use_case.get_password_hash") as mock_get_hash:
            mock_get_hash.return_value = "hashed_password"

            # Configure the add method to return a user
            mock_user = User(
                id=1,
                username=self.user_data.username,
                email=self.user_data.email,
                password="hashed_password",
                cpf=self.user_data.cpf
            )
            self.user_repository.add.return_value = mock_user

            # Act
            result = self.use_case.execute(self.user_data)

            # Assert
            self.user_repository.get_by_username_or_email_or_cpf.assert_called_once_with(
                self.user_data.username, self.user_data.email, self.user_data.cpf
            )
            mock_get_hash.assert_called_once_with(self.user_data.password)
            self.user_repository.add.assert_called_once()
            assert isinstance(result, User)
            assert result.username == self.user_data.username
            assert result.email == self.user_data.email
            assert result.password == "hashed_password"
            assert result.cpf == self.user_data.cpf

    def test_invalid_cpf_format(self):
        """Test that an invalid CPF format raises a ValueError."""
        # Arrange
        invalid_user_data = UserSchema(
            username="testuser",
            email="test@example.com",
            password="Password123",
            cpf="123456"  # Too short
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.use_case.execute(invalid_user_data)

        assert "CPF must contain exactly 11 digits" in str(exc_info.value)
        self.user_repository.get_by_username_or_email_or_cpf.assert_not_called()
        self.user_repository.add.assert_not_called()

    def test_non_numeric_cpf(self):
        """Test that a non-numeric CPF raises a ValueError."""
        # Arrange
        invalid_user_data = UserSchema(
            username="testuser",
            email="test@example.com",
            password="Password123",
            cpf="1234567890a"  # Contains a letter
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.use_case.execute(invalid_user_data)

        assert "CPF must contain exactly 11 digits and be numeric" in str(exc_info.value)

    def test_user_already_exists(self):
        """Test that trying to create a user that already exists raises a ValueError."""
        # Arrange
        existing_user = User(
            id=1,
            username="existinguser",
            email="existing@example.com",
            password="hashed_password",
            cpf="12345678901"
        )
        self.user_repository.get_by_username_or_email_or_cpf.return_value = existing_user

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.use_case.execute(self.user_data)

        assert "User already exists" in str(exc_info.value)
        self.user_repository.add.assert_not_called()