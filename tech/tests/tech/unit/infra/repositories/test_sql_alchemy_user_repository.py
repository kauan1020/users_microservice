# tests/unit/infra/repositories/test_sql_alchemy_user_repository.py
import pytest
from unittest.mock import Mock, patch, MagicMock
from sqlalchemy import select
from tech.domain.entities.users import User
from tech.infra.repositories.sql_alchemy_user_repository import SQLAlchemyUserRepository
from tech.infra.repositories.sql_alchemy_models import SQLAlchemyUser


class TestSQLAlchemyUserRepository:
    """Unit tests for the SQLAlchemyUserRepository."""

    def setup_method(self):
        """Set up test dependencies."""
        self.mock_session = Mock()
        self.repository = SQLAlchemyUserRepository(self.mock_session)

        # Create a sample domain user
        self.domain_user = User(
            id=1,
            username="testuser",
            email="test@example.com",
            password="hashed_password",
            cpf="12345678901"
        )

        # Create a sample SQLAlchemy model instance
        self.db_user = Mock(spec=SQLAlchemyUser)
        self.db_user.id = 1
        self.db_user.username = "testuser"
        self.db_user.email = "test@example.com"
        self.db_user.password = "hashed_password"
        self.db_user.cpf = "12345678901"

    def test_to_domain_user(self):
        """Test conversion from SQLAlchemy model to domain entity."""
        # Act
        domain_user = self.repository._to_domain_user(self.db_user)

        # Assert
        assert isinstance(domain_user, User)
        assert domain_user.id == self.db_user.id
        assert domain_user.username == self.db_user.username
        assert domain_user.email == self.db_user.email
        assert domain_user.password == self.db_user.password
        assert domain_user.cpf == self.db_user.cpf

    @patch('tech.infra.repositories.sql_alchemy_user_repository.SQLAlchemyUser')
    def test_add_user(self, mock_user_class):
        """Test adding a new user to the database."""
        # Arrange
        mock_user_class.return_value = self.db_user

        # Act
        result = self.repository.add(self.domain_user)

        # Assert
        # Check that SQLAlchemyUser was instantiated with correct parameters
        mock_user_class.assert_called_once()

        # Check repository operations
        self.mock_session.add.assert_called_once_with(self.db_user)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(self.db_user)

        # Check the result
        assert result == self.domain_user
        assert result.id == self.db_user.id  # ID should be updated

    def test_get_by_id_found(self):
        """Test retrieving a user by ID when found."""
        # Arrange
        self.mock_session.scalar.return_value = self.db_user

        # Act
        result = self.repository.get_by_id(1)

        # Assert
        assert isinstance(result, User)
        assert result.id == 1
        assert result.username == "testuser"

        # Verify select query
        self.mock_session.scalar.assert_called_once()
        # The 'select' instance check is removed as it causes TypeError

    def test_get_by_id_not_found(self):
        """Test retrieving a user by ID when not found."""
        # Arrange
        self.mock_session.scalar.return_value = None

        # Act
        result = self.repository.get_by_id(999)

        # Assert
        assert result is None
        self.mock_session.scalar.assert_called_once()

    def test_get_by_username_or_email_or_cpf_found(self):
        """Test retrieving a user by username, email, or CPF when found."""
        # Arrange
        self.mock_session.scalar.return_value = self.db_user

        # Act
        result = self.repository.get_by_username_or_email_or_cpf(
            username="testuser",
            email="test@example.com",
            cpf="12345678901"
        )

        # Assert
        assert isinstance(result, User)
        assert result.id == 1
        assert result.username == "testuser"

        # Verify select query
        self.mock_session.scalar.assert_called_once()
        # The 'select' instance check is removed as it causes TypeError

    def test_get_by_username_or_email_or_cpf_not_found(self):
        """Test retrieving a user by username, email, or CPF when not found."""
        # Arrange
        self.mock_session.scalar.return_value = None

        # Act
        result = self.repository.get_by_username_or_email_or_cpf(
            username="nonexistent",
            email="nonexistent@example.com",
            cpf="99999999999"
        )

        # Assert
        assert result is None
        self.mock_session.scalar.assert_called_once()

    def test_get_by_cpf_found(self):
        """Test retrieving a user by CPF when found."""
        # Arrange
        self.mock_session.scalar.return_value = self.db_user

        # Act
        result = self.repository.get_by_cpf("12345678901")

        # Assert
        assert isinstance(result, User)
        assert result.id == 1
        assert result.cpf == "12345678901"

        # Verify select query
        self.mock_session.scalar.assert_called_once()
        # The 'select' instance check is removed as it causes TypeError

    def test_get_by_cpf_not_found(self):
        """Test retrieving a user by CPF when not found."""
        # Arrange
        self.mock_session.scalar.return_value = None

        # Act
        result = self.repository.get_by_cpf("99999999999")

        # Assert
        assert result is None
        self.mock_session.scalar.assert_called_once()

    def test_list_users(self):
        """Test listing users with pagination."""
        # Arrange
        db_users = [self.db_user, Mock(spec=SQLAlchemyUser)]
        db_users[1].id = 2
        db_users[1].username = "user2"
        db_users[1].email = "user2@example.com"
        db_users[1].password = "hashed_password2"
        db_users[1].cpf = "98765432101"

        # Mock the .all() result on the scalars query result
        scalar_result = MagicMock()
        scalar_result.all.return_value = db_users
        self.mock_session.scalars.return_value = scalar_result

        # Act
        result = self.repository.list_users(limit=10, skip=0)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(user, User) for user in result)
        assert result[0].id == 1
        assert result[1].id == 2

        # Verify query
        self.mock_session.scalars.assert_called_once()
        # The 'select' instance check is removed as it causes TypeError

    def test_update_user_found(self):
        """Test updating a user when found."""
        # Arrange
        self.mock_session.scalar.return_value = self.db_user

        # Update the domain user
        updated_user = User(
            id=1,
            username="updated_user",
            email="updated@example.com",
            password="new_password",
            cpf="12345678901"
        )

        # Act
        result = self.repository.update(updated_user)

        # Assert
        # Check the db_user was updated correctly
        assert self.db_user.username == "updated_user"
        assert self.db_user.email == "updated@example.com"
        assert self.db_user.password == "new_password"
        assert self.db_user.cpf == "12345678901"

        # Check repository operations
        self.mock_session.scalar.assert_called_once()
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(self.db_user)

        # Check the result
        assert result == updated_user

    def test_update_user_not_found(self):
        """Test updating a user when not found."""
        # Arrange
        self.mock_session.scalar.return_value = None

        # Act
        result = self.repository.update(self.domain_user)

        # Assert
        self.mock_session.scalar.assert_called_once()
        self.mock_session.commit.assert_not_called()
        self.mock_session.refresh.assert_not_called()
        assert result == self.domain_user  # Should return the original user

    def test_delete_user_found(self):
        """Test deleting a user when found."""
        # Arrange
        self.mock_session.scalar.return_value = self.db_user

        # Act
        self.repository.delete(self.domain_user)

        # Assert
        self.mock_session.scalar.assert_called_once()
        self.mock_session.delete.assert_called_once_with(self.db_user)
        self.mock_session.commit.assert_called_once()

    def test_delete_user_not_found(self):
        """Test deleting a user when not found."""
        # Arrange
        self.mock_session.scalar.return_value = None

        # Act
        self.repository.delete(self.domain_user)

        # Assert
        self.mock_session.scalar.assert_called_once()
        self.mock_session.delete.assert_not_called()
        self.mock_session.commit.assert_not_called()