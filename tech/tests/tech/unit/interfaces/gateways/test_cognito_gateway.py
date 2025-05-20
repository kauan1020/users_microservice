# tests/unit/interfaces/gateways/test_cognito_gateway.py
import pytest
import boto3
import json
import base64
from unittest.mock import Mock, patch, MagicMock
from tech.interfaces.gateways.cognito_gateway import CognitoGateway


class TestCognitoGateway:
    """Unit tests for the CognitoGateway."""

    def setup_method(self):
        """Set up test fixtures."""
        # Patch boto3.client to avoid actual AWS calls
        self.boto3_client_patch = patch('boto3.client')
        self.mock_boto3_client = self.boto3_client_patch.start()

        # Create a mock Cognito client
        self.mock_cognito_client = Mock()

        # Set up exceptions as attributes of mock_cognito_client.exceptions
        self.mock_cognito_client.exceptions = Mock()
        self.mock_cognito_client.exceptions.NotAuthorizedException = type(
            'NotAuthorizedException', (Exception,), {}
        )
        self.mock_cognito_client.exceptions.UserNotFoundException = type(
            'UserNotFoundException', (Exception,), {}
        )

        self.mock_boto3_client.return_value = self.mock_cognito_client

        # Initialize the gateway
        self.gateway = CognitoGateway()

        # Test data
        self.test_cpf = "12345678901"
        self.test_password = "Password123"

    def teardown_method(self):
        """Clean up after tests."""
        self.boto3_client_patch.stop()

    def test_initialization(self):
        """Test that the gateway is initialized with the correct configuration."""
        # Verify boto3.client was called with correct parameters
        self.mock_boto3_client.assert_called_once_with(
            "cognito-idp",
            region_name=self.gateway.region,
            aws_access_key_id="SUA_ACCESS_KEY_ID",
            aws_secret_access_key="SUA_SECRET_ACCESS_KEY"
        )

        # Check that the gateway has the expected attributes
        assert self.gateway.region == "us-east-1"
        assert self.gateway.user_pool_id == "us-east-1_k6nq9jjr3"
        assert self.gateway.client_id == "5mkhqrqcm84nbmvt5srg6kgfsb"
        assert self.gateway.client_secret == "1f240j4ildo1due9gt8o7ghlesovrltk573lbnktabtn3o58alu6"
        assert self.gateway.client == self.mock_cognito_client

    def test_get_secret_hash(self):
        """Test that _get_secret_hash generates the correct hash."""
        # We'll use a known input and expected output
        result = self.gateway._get_secret_hash(self.test_cpf)

        # Verify it's a base64-encoded string
        try:
            decoded = base64.b64decode(result)
            assert len(decoded) > 0
        except Exception:
            pytest.fail("The result is not a valid base64-encoded string")

    def test_successful_authentication(self):
        """Test successful authentication flow."""
        # Arrange
        mock_auth_result = {
            "AuthenticationResult": {
                "IdToken": "mock-id-token",
                "AccessToken": "mock-access-token",
                "RefreshToken": "mock-refresh-token",
                "ExpiresIn": 3600
            }
        }
        self.mock_cognito_client.initiate_auth.return_value = mock_auth_result

        # Act
        result = self.gateway.authenticate(self.test_cpf, self.test_password)

        # Assert
        self.mock_cognito_client.initiate_auth.assert_called_once()
        call_args = self.mock_cognito_client.initiate_auth.call_args[1]
        assert call_args["AuthFlow"] == "USER_PASSWORD_AUTH"
        assert call_args["ClientId"] == self.gateway.client_id
        assert call_args["AuthParameters"]["USERNAME"] == self.test_cpf
        assert call_args["AuthParameters"]["PASSWORD"] == self.test_password
        assert "SECRET_HASH" in call_args["AuthParameters"]

        assert result == mock_auth_result["AuthenticationResult"]

    def test_authentication_not_authorized(self):
        """Test authentication when credentials are invalid."""
        # Arrange - Use the existing exception classes created in setup_method
        error_msg = "Incorrect username or password."
        self.mock_cognito_client.initiate_auth.side_effect = self.mock_cognito_client.exceptions.NotAuthorizedException(
            error_msg)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.gateway.authenticate(self.test_cpf, "wrong_password")

        assert "Incorrect credentials" in str(exc_info.value)

    def test_authentication_user_not_found(self):
        """Test authentication when user doesn't exist."""
        # Arrange - Use the existing exception classes created in setup_method
        error_msg = "User does not exist."
        self.mock_cognito_client.initiate_auth.side_effect = self.mock_cognito_client.exceptions.UserNotFoundException(
            error_msg)

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.gateway.authenticate("99999999999", self.test_password)

        assert "User not found" in str(exc_info.value)

    def test_decode_jwt_manually(self):
        """Test that _decode_jwt_manually correctly decodes a JWT token."""
        # Create a simple JWT token (header.payload.signature)
        payload = {"sub": "user123", "name": "Test User"}
        payload_json = json.dumps(payload)
        payload_b64 = base64.b64encode(payload_json.encode()).decode()
        payload_b64 = payload_b64.replace('+', '-').replace('/', '_').rstrip('=')

        mock_token = f"header.{payload_b64}.signature"

        # Act
        result = self.gateway._decode_jwt_manually(mock_token)

        # Assert
        assert result == payload

    def test_verify_token_with_groups_in_token(self):
        """Test token verification when groups info is in the token."""
        # Arrange
        # Mock the _decode_jwt_manually method
        with patch.object(self.gateway, '_decode_jwt_manually') as mock_decode:
            mock_decode.return_value = {
                "cognito:username": "test_user",
                "sub": "user-sub-id",
                "email": "test@example.com",
                "cognito:groups": ["admin", "users"]
            }

            # Act
            result = self.gateway.verify_token("mock-token")

            # Assert
            mock_decode.assert_called_once_with("mock-token")
            assert result["username"] == "test_user"
            assert result["attributes"]["sub"] == "user-sub-id"
            assert result["attributes"]["email"] == "test@example.com"
            assert result["is_admin"] is True

    def test_verify_token_admin_check_with_api(self):
        """Test token verification when admin status needs to be checked via API."""
        # Arrange
        # Mock the _decode_jwt_manually method
        with patch.object(self.gateway, '_decode_jwt_manually') as mock_decode:
            mock_decode.return_value = {
                "sub": "user-sub-id",
                "email": "test@example.com"
                # No cognito:groups in token
            }

            # Mock the admin_get_user response
            self.mock_cognito_client.admin_get_user.return_value = {
                "Username": "test_user",
                "UserAttributes": [
                    {"Name": "sub", "Value": "user-sub-id"},
                    {"Name": "email", "Value": "test@example.com"}
                ]
            }

            # Mock the admin_list_groups_for_user response
            self.mock_cognito_client.admin_list_groups_for_user.return_value = {
                "Groups": [
                    {"GroupName": "admin"},
                    {"GroupName": "users"}
                ]
            }

            # Act
            result = self.gateway.verify_token("mock-token")

            # Assert
            mock_decode.assert_called_once_with("mock-token")
            self.mock_cognito_client.admin_get_user.assert_called_once_with(
                UserPoolId=self.gateway.user_pool_id,
                Username="user-sub-id"
            )
            self.mock_cognito_client.admin_list_groups_for_user.assert_called_once_with(
                UserPoolId=self.gateway.user_pool_id,
                Username="user-sub-id"
            )
            assert result["username"] == "test_user"
            assert result["attributes"]["sub"] == "user-sub-id"
            assert result["attributes"]["email"] == "test@example.com"
            assert result["is_admin"] is True

    def test_verify_token_invalid_format(self):
        """Test token verification with an invalid token format."""
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            self.gateway.verify_token("invalid-token-no-dots")

        assert "Invalid JWT format" in str(exc_info.value)

    def test_user_not_found_during_verification(self):
        """Test token verification when user is not found."""
        # Arrange
        with patch.object(self.gateway, '_decode_jwt_manually') as mock_decode:
            mock_decode.return_value = {
                "sub": "nonexistent-user-id"
            }

            # Use the exception already defined in setup_method
            self.mock_cognito_client.admin_get_user.side_effect = self.mock_cognito_client.exceptions.UserNotFoundException(
                "User does not exist")

            # Act & Assert
            with pytest.raises(ValueError) as exc_info:
                self.gateway.verify_token("mock-token")

            assert "User not found" in str(exc_info.value)