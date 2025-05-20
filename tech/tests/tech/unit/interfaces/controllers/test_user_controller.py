import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from tech.interfaces.controllers.user_controller import UserController
from tech.use_cases.users.create_user_use_case import CreateUserUseCase
from tech.use_cases.users.list_users_use_case import ListUsersUseCase
from tech.use_cases.users.get_user_use_case import GetUserUseCase
from tech.use_cases.users.get_user_by_cpf_use_case import GetUserByCpfUseCase
from tech.use_cases.users.update_user_use_case import UpdateUserUseCase
from tech.use_cases.users.delete_user_use_case import DeleteUserUseCase
from tech.interfaces.schemas.user_schema import UserSchema
from tech.domain.entities.users import User


class TestUserController:
    def setup_method(self):
        # Cria mocks para os use cases
        self.create_user_use_case = Mock(spec=CreateUserUseCase)
        self.list_users_use_case = Mock(spec=ListUsersUseCase)
        self.get_user_use_case = Mock(spec=GetUserUseCase)
        self.get_user_by_cpf_use_case = Mock(spec=GetUserByCpfUseCase)
        self.update_user_use_case = Mock(spec=UpdateUserUseCase)
        self.delete_user_use_case = Mock(spec=DeleteUserUseCase)

        self.controller = UserController(
            self.create_user_use_case,
            self.list_users_use_case,
            self.get_user_use_case,
            self.get_user_by_cpf_use_case,
            self.update_user_use_case,
            self.delete_user_use_case
        )

        # Mock de usuário para testes
        self.mock_user = Mock(spec=User)
        self.mock_user.id = 1
        self.mock_user.username = "testuser"
        self.mock_user.email = "test@example.com"
        self.mock_user.cpf = "12345678901"

        # Mock de esquema de usuário para testes
        self.user_data = UserSchema(
            username="testuser",
            email="test@example.com",
            password="password123",
            cpf="12345678901"
        )

    @patch("tech.interfaces.presenters.user_presenter.UserPresenter.present_user")
    def test_create_user_success(self, mock_present_user):
        # Arrange
        self.create_user_use_case.execute.return_value = self.mock_user
        expected_response = {"id": 1, "username": "testuser", "email": "test@example.com", "cpf": "12345678901"}
        mock_present_user.return_value = expected_response

        # Act
        result = self.controller.create_user(self.user_data)

        # Assert
        self.create_user_use_case.execute.assert_called_once_with(self.user_data)
        mock_present_user.assert_called_once_with(self.mock_user)
        assert result == expected_response

    def test_create_user_error(self):
        # Arrange
        error_message = "User already exists"
        self.create_user_use_case.execute.side_effect = ValueError(error_message)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.controller.create_user(self.user_data)

        # Verify
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == error_message
        self.create_user_use_case.execute.assert_called_once_with(self.user_data)

    @patch("tech.interfaces.presenters.user_presenter.UserPresenter.present_user_list")
    def test_list_users(self, mock_present_user_list):
        # Arrange
        mock_users = [self.mock_user, Mock(spec=User)]
        self.list_users_use_case.execute.return_value = mock_users
        expected_response = [
            {"id": 1, "username": "testuser", "email": "test@example.com", "cpf": "12345678901"},
            {"id": 2, "username": "user2", "email": "user2@example.com", "cpf": "98765432101"}
        ]
        mock_present_user_list.return_value = expected_response

        # Act
        result = self.controller.list_users(10, 0)

        # Assert
        self.list_users_use_case.execute.assert_called_once_with(10, 0)
        mock_present_user_list.assert_called_once_with(mock_users)
        assert result == expected_response

    @patch("tech.interfaces.presenters.user_presenter.UserPresenter.present_user")
    def test_get_user_success(self, mock_present_user):
        # Arrange
        self.get_user_use_case.execute.return_value = self.mock_user
        expected_response = {"id": 1, "username": "testuser", "email": "test@example.com", "cpf": "12345678901"}
        mock_present_user.return_value = expected_response

        # Act
        result = self.controller.get_user(1)

        # Assert
        self.get_user_use_case.execute.assert_called_once_with(1)
        mock_present_user.assert_called_once_with(self.mock_user)
        assert result == expected_response

    def test_get_user_not_found(self):
        # Arrange
        error_message = "User not found"
        self.get_user_use_case.execute.side_effect = ValueError(error_message)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.controller.get_user(999)

        # Verify
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == error_message
        self.get_user_use_case.execute.assert_called_once_with(999)

    @patch("tech.interfaces.presenters.user_presenter.UserPresenter.present_user")
    def test_get_user_by_cpf_success(self, mock_present_user):
        # Arrange
        self.get_user_by_cpf_use_case.execute.return_value = self.mock_user
        expected_response = {"id": 1, "username": "testuser", "email": "test@example.com", "cpf": "12345678901"}
        mock_present_user.return_value = expected_response

        # Act
        result = self.controller.get_user_by_cpf("12345678901")

        # Assert
        self.get_user_by_cpf_use_case.execute.assert_called_once_with("12345678901")
        mock_present_user.assert_called_once_with(self.mock_user)
        assert result == expected_response

    def test_get_user_by_cpf_not_found(self):
        # Arrange
        error_message = "User not found"
        self.get_user_by_cpf_use_case.execute.side_effect = ValueError(error_message)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.controller.get_user_by_cpf("99999999999")

        # Verify
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == error_message
        self.get_user_by_cpf_use_case.execute.assert_called_once_with("99999999999")

    @patch("tech.interfaces.presenters.user_presenter.UserPresenter.present_user")
    def test_update_user_success(self, mock_present_user):
        # Arrange
        self.update_user_use_case.execute.return_value = self.mock_user
        expected_response = {"id": 1, "username": "testuser", "email": "test@example.com", "cpf": "12345678901"}
        mock_present_user.return_value = expected_response

        # Act
        result = self.controller.update_user(1, self.user_data)

        # Assert
        self.update_user_use_case.execute.assert_called_once_with(1, self.user_data)
        mock_present_user.assert_called_once_with(self.mock_user)
        assert result == expected_response

    def test_update_user_not_found(self):
        # Arrange
        error_message = "User not found"
        self.update_user_use_case.execute.side_effect = ValueError(error_message)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.controller.update_user(999, self.user_data)

        # Verify
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == error_message
        self.update_user_use_case.execute.assert_called_once_with(999, self.user_data)

    def test_delete_user_success(self):
        # Arrange
        success_message = {"message": "User deleted"}
        self.delete_user_use_case.execute.return_value = success_message

        # Act
        result = self.controller.delete_user(1)

        # Assert
        self.delete_user_use_case.execute.assert_called_once_with(1)
        assert result == success_message

    def test_delete_user_not_found(self):
        # Arrange
        error_message = "User not found"
        self.delete_user_use_case.execute.side_effect = ValueError(error_message)

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            self.controller.delete_user(999)

        # Verify
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == error_message
        self.delete_user_use_case.execute.assert_called_once_with(999)