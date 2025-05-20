# from tech.interfaces.middlewares.admin_auth_middleware import admin_required
# import pytest
# from unittest.mock import Mock, patch
# from fastapi import HTTPException
# from fastapi.security import HTTPAuthorizationCredentials
# from tech.interfaces.gateways.cognito_gateway import CognitoGateway
#
#
# class TestAdminRequired:
#     """Unit tests for the admin_required middleware."""
#
#     def setup_method(self):
#         """Set up test fixtures."""
#         self.mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
#         self.mock_credentials.credentials = "valid-token"
#
#         self.mock_cognito_gateway = Mock(spec=CognitoGateway)
#
#     @patch("tech.interfaces.gateways.cognito_gateway.CognitoGateway")
#     def test_admin_access_allowed(self, mock_cognito_class):
#         """Test that admin users are allowed access."""
#         # Arrange
#         mock_cognito_instance = mock_cognito_class.return_value
#
#         # Configure the mock to return admin user data
#         mock_cognito_instance.verify_token.return_value = {
#             "username": "admin_user",
#             "is_admin": True
#         }
#
#         # Act
#         result = admin_required(self.mock_credentials)
#
#         # Assert
#         mock_cognito_instance.verify_token.assert_called_once_with(self.mock_credentials.credentials)
#         assert result is True
#
#     @patch("tech.interfaces.gateways.cognito_gateway.CognitoGateway")
#     def test_non_admin_access_denied(self, mock_cognito_class):
#         """Test that non-admin users are denied access."""
#         # Arrange
#         mock_cognito_instance = mock_cognito_class.return_value
#
#         # Configure the mock to return non-admin user data
#         mock_cognito_instance.verify_token.return_value = {
#             "username": "regular_user",
#             "is_admin": False
#         }
#
#         # Act & Assert
#         with pytest.raises(HTTPException) as exc_info:
#             admin_required(self.mock_credentials)
#
#         # Check status code and detail
#         assert exc_info.value.status_code == 403
#         assert "Insufficient permissions" in exc_info.value.detail
#
#     @patch("tech.interfaces.gateways.cognito_gateway.CognitoGateway")
#     def test_invalid_token(self, mock_cognito_class):
#         """Test that invalid tokens raise a 401 Unauthorized exception."""
#         # Arrange
#         mock_cognito_instance = mock_cognito_class.return_value
#
#         # Configure the mock to raise an error for invalid token
#         mock_cognito_instance.verify_token.side_effect = ValueError("Invalid token")
#
#         # Act & Assert
#         with pytest.raises(HTTPException) as exc_info:
#             admin_required(self.mock_credentials)
#
#         # Check status code and detail
#         assert exc_info.value.status_code == 401
#         assert "Invalid authentication credentials" in exc_info.value.detail
#
#     def test_missing_credentials(self):
#         """Test that missing credentials raise a 401 Unauthorized exception."""
#         # Arrange
#         credentials = None
#
#         # Act & Assert
#         with pytest.raises(HTTPException) as exc_info:
#             admin_required(credentials)
#
#         # Check status code and detail
#         assert exc_info.value.status_code == 401
#         assert "Authentication credentials not provided" in exc_info.value.detail
#
#     @patch("tech.interfaces.gateways.cognito_gateway.CognitoGateway")
#     def test_empty_token(self, mock_cognito_class):
#         """Test that empty tokens raise a validation error."""
#         # Arrange
#         credentials = Mock(spec=HTTPAuthorizationCredentials)
#         credentials.credentials = ""
#
#         # Act & Assert
#         with pytest.raises(HTTPException) as exc_info:
#             admin_required(credentials)
#
#         # Check status code and detail
#         assert exc_info.value.status_code == 401
#         assert "Token must be a non-empty string" in exc_info.value.detail
#
#         # Verify the gateway was not used
#         mock_cognito_class.assert_not_called()