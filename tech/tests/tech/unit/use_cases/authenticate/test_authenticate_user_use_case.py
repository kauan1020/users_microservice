import pytest
from unittest.mock import Mock, patch
from tech.interfaces.schemas.auth_schema import AuthRequest, AuthResponse
from tech.interfaces.gateways.cognito_gateway import CognitoGateway
from tech.use_cases.authenticate.authenticate_user_use_case import AuthenticateUserUseCase


class TestAuthenticateUserUseCase:
    """Unit tests for the AuthenticateUserUseCase."""

    def setup_method(self):
        """Set up test dependencies."""
        self.cognito_gateway = Mock(spec=CognitoGateway)
        self.use_case = AuthenticateUserUseCase(self.cognito_gateway)
        self.auth_request = AuthRequest(cpf="12345678901", password="password123")

    def test_successful_authentication(self):
        """Test that the use case returns the correct response on successful authentication."""
        # Arrange
        mock_auth_result = {
            "IdToken": "sample-token-value",
            "ExpiresIn": 3600
        }
        self.cognito_gateway.authenticate.return_value = mock_auth_result

        # Act
        result = self.use_case.execute(self.auth_request)

        # Assert
        self.cognito_gateway.authenticate.assert_called_once_with(
            self.auth_request.cpf,
            self.auth_request.password
        )
        assert isinstance(result, AuthResponse)
        assert result.token == "sample-token-value"
        assert result.expires_in == 3600

    def test_authentication_failure_from_gateway(self):
        """Test that the use case properly handles errors from the gateway."""
        # Arrange
        self.cognito_gateway.authenticate.side_effect = ValueError("Invalid credentials")

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.use_case.execute(self.auth_request)

        assert "Invalid credentials" in str(exc_info.value)
        self.cognito_gateway.authenticate.assert_called_once()

    def test_empty_auth_result(self):
        """Test that the use case handles empty auth results correctly."""
        # Arrange
        self.cognito_gateway.authenticate.return_value = {}

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.use_case.execute(self.auth_request)

        assert "empty response" in str(exc_info.value)

    def test_unexpected_exception_handling(self):
        """Test that the use case handles unexpected exceptions."""
        # Arrange
        self.cognito_gateway.authenticate.side_effect = Exception("Network error")

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.use_case.execute(self.auth_request)

        assert "Authentication failed: Network error" in str(exc_info.value)
