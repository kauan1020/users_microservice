import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from tech.interfaces.controllers.auth_controller import AuthController
from tech.interfaces.schemas.auth_schema import AuthRequest, AuthResponse


@pytest.fixture
def mock_router():
    app = FastAPI()

    mock_controller = Mock(spec=AuthController)

    mock_controller.authenticate.return_value = AuthResponse(
        token="test-token",
        expires_in=3600
    )

    @app.post("/auth/login")
    def login(auth_request: AuthRequest):
        try:
            return mock_controller.authenticate(auth_request)
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))

    client = TestClient(app)

    return {
        "app": app,
        "client": client,
        "controller": mock_controller
    }


class TestAuthRouter:
    """Unit tests for the auth router."""

    def test_login_successful(self, mock_router):
        """Test successful login through the API endpoint."""
        client = mock_router["client"]
        controller = mock_router["controller"]

        # Act
        response = client.post(
            "/auth/login",
            json={"cpf": "12345678901", "password": "password123"}
        )

        # Assert
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
        response_data = response.json()
        assert response_data["token"] == "test-token"
        assert response_data["expires_in"] == 3600

        # Verify controller call
        controller.authenticate.assert_called_once()
        auth_request = controller.authenticate.call_args[0][0]
        assert auth_request.cpf == "12345678901"
        assert auth_request.password == "password123"

    def test_login_failure(self, mock_router):
        """Test login failure handling through the API endpoint."""
        client = mock_router["client"]
        controller = mock_router["controller"]

        # Configurar erro
        controller.authenticate.side_effect = ValueError("Invalid credentials")

        # Act
        response = client.post(
            "/auth/login",
            json={"cpf": "12345678901", "password": "wrong_password"}
        )

        # Assert
        assert response.status_code == 401
        response_data = response.json()
        assert "Invalid credentials" in response_data["detail"]

        # Verify controller call
        controller.authenticate.assert_called_once()

    def test_login_with_invalid_data(self, mock_router):
        """Test login with invalid request data."""
        client = mock_router["client"]

        # Act - missing password
        response = client.post(
            "/auth/login",
            json={"cpf": "12345678901"}
        )

        # Assert
        assert response.status_code == 422  # Unprocessable Entity

        # Act - invalid JSON
        response = client.post(
            "/auth/login",
            data="invalid json data"
        )

        # Assert
        assert response.status_code == 422


@patch("tech.interfaces.gateways.cognito_gateway.CognitoGateway")
@patch("tech.use_cases.authenticate.authenticate_user_use_case.AuthenticateUserUseCase")
def test_get_auth_controller_dependency(mock_use_case_class, mock_cognito_class):
    """Test the get_auth_controller dependency function directly."""
    from tech.api.auth_router import get_auth_controller

    mock_cognito = Mock()
    mock_use_case = Mock()
    mock_cognito_class.return_value = mock_cognito
    mock_use_case_class.return_value = mock_use_case

    mock_session = Mock()

    controller = get_auth_controller(session=mock_session)

    assert isinstance(controller, AuthController)
    mock_cognito_class.assert_called_once()
    mock_use_case_class.assert_called_once_with(mock_cognito)