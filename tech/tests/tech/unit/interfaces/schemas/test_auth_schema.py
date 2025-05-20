# tests/unit/interfaces/schemas/test_auth_schema.py
import pytest
from pydantic import ValidationError
from tech.interfaces.schemas.auth_schema import AuthRequest, AuthResponse


class TestAuthRequest:
    """Unit tests for the AuthRequest schema."""

    def test_valid_auth_request(self):
        """Test creating a valid authentication request."""
        # Arrange
        data = {
            "cpf": "12345678901",
            "password": "secure_password"
        }

        # Act
        auth_request = AuthRequest(**data)

        # Assert
        assert auth_request.cpf == "12345678901"
        assert auth_request.password == "secure_password"

    def test_missing_cpf(self):
        """Test that CPF is required."""
        # Arrange
        data = {
            "password": "secure_password"
        }

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            AuthRequest(**data)

        # Check error details
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("cpf",)
        assert "Field required" in errors[0]["msg"]

    def test_missing_password(self):
        """Test that password is required."""
        # Arrange
        data = {
            "cpf": "12345678901"
        }

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            AuthRequest(**data)

        # Check error details
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("password",)
        assert "Field required" in errors[0]["msg"]

    def test_empty_cpf(self):
        """Test that CPF can be empty."""
        # Arrange
        data = {
            "cpf": "",
            "password": "secure_password"
        }

        # Act
        auth_request = AuthRequest(**data)

        # Assert - Pydantic allows empty strings by default
        assert auth_request.cpf == ""

    def test_empty_password(self):
        """Test that password can be empty."""
        # Arrange
        data = {
            "cpf": "12345678901",
            "password": ""
        }

        # Act
        auth_request = AuthRequest(**data)

        # Assert - Pydantic allows empty strings by default
        assert auth_request.password == ""

    def test_conversion_to_dict(self):
        """Test converting AuthRequest to dictionary."""
        # Arrange
        auth_request = AuthRequest(
            cpf="12345678901",
            password="secure_password"
        )

        # Act
        data = auth_request.dict()

        # Assert
        assert isinstance(data, dict)
        assert data == {
            "cpf": "12345678901",
            "password": "secure_password"
        }


class TestAuthResponse:
    """Unit tests for the AuthResponse schema."""

    def test_valid_auth_response(self):
        """Test creating a valid authentication response."""
        # Arrange
        data = {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "expires_in": 3600
        }

        # Act
        auth_response = AuthResponse(**data)

        # Assert
        assert auth_response.token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        assert auth_response.expires_in == 3600

    def test_additional_fields_allowed(self):
        """Test that additional fields are allowed in AuthResponse."""
        # Arrange
        data = {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "expires_in": 3600,
            "refresh_token": "refresh-token-value",
            "token_type": "Bearer"
        }

        # Act
        auth_response = AuthResponse(**data)

        # Assert
        assert auth_response.token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        assert auth_response.expires_in == 3600
        assert auth_response.refresh_token == "refresh-token-value"
        assert auth_response.token_type == "Bearer"

    def test_missing_token(self):
        """Test that token is required."""
        # Arrange
        data = {
            "expires_in": 3600
        }

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            AuthResponse(**data)

        # Check error details
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("token",)
        assert "Field required" in errors[0]["msg"]

    def test_missing_expires_in(self):
        """Test that expires_in is required."""
        # Arrange
        data = {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            AuthResponse(**data)

        # Check error details
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]["loc"] == ("expires_in",)
        assert "Field required" in errors[0]["msg"]


    def test_json_serialization(self):
        """Test JSON serialization of AuthResponse."""
        # Arrange
        auth_response = AuthResponse(
            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            expires_in=3600,
            refresh_token="refresh-token-value"
        )

        # Act
        json_data = auth_response.json()

        # Assert
        assert isinstance(json_data, str)
        assert "token" in json_data
        assert "expires_in" in json_data
        assert "refresh_token" in json_data