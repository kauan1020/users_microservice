# tests/integration/steps/auth_steps.py
from behave import given, when, then
from unittest.mock import Mock, patch
import json


@given('the system has a registered user with CPF "{cpf}" and password "{password}"')
def step_impl(context, cpf, password):
    """Set up a registered user in the system."""
    # Store the registered user for later steps
    context.registered_users = getattr(context, 'registered_users', {})
    context.registered_users[cpf] = {
        'password': password,
        'id': 1,
        'username': 'testuser',
        'email': 'test@example.com'
    }


@when('the user attempts to log in with CPF "{cpf}" and password "{password}"')
def step_impl(context, cpf, password):
    """Simulate a login attempt."""
    from tech.interfaces.schemas.auth_schema import AuthRequest

    # Create the auth request
    auth_request = AuthRequest(cpf=cpf, password=password)

    # Store the request for later steps
    context.auth_request = auth_request

    # Mock the CognitoGateway
    with patch('tech.interfaces.gateways.cognito_gateway.CognitoGateway') as mock_cognito_class:
        mock_cognito = Mock()
        mock_cognito_class.return_value = mock_cognito

        # Configure the mock based on whether the login should succeed
        if (cpf in context.registered_users and
                context.registered_users[cpf]['password'] == password):
            # Successful login
            mock_cognito.authenticate.return_value = {
                "IdToken": "mock-jwt-token",
                "ExpiresIn": 3600,
                "RefreshToken": "mock-refresh-token"
            }
            context.login_successful = True
        else:
            # Failed login
            if cpf not in context.registered_users:
                error_message = "User not found"
            else:
                error_message = "Incorrect credentials"
            mock_cognito.authenticate.side_effect = ValueError(error_message)
            context.login_successful = False
            context.error_message = error_message

        # Create the use case with the mocked gateway
        from tech.use_cases.authenticate.authenticate_user_use_case import AuthenticateUserUseCase
        auth_use_case = AuthenticateUserUseCase(mock_cognito)

        # Create the controller with the use case
        from tech.interfaces.controllers.auth_controller import AuthController
        auth_controller = AuthController(auth_use_case)

        # Try to authenticate
        try:
            context.auth_response = auth_controller.authenticate(auth_request)
            context.auth_token = context.auth_response.token
        except ValueError as e:
            context.error = str(e)


@then('the login should be successful')
def step_impl(context):
    """Verify that the login was successful."""
    assert context.login_successful is True
    assert hasattr(context, 'auth_response')
    assert not hasattr(context, 'error')


@then('the login should fail')
def step_impl(context):
    """Verify that the login failed."""
    assert context.login_successful is False
    assert hasattr(context, 'error')


@then('the user should receive a valid token')
def step_impl(context):
    """Verify that a valid token was received."""
    assert hasattr(context, 'auth_response')
    assert hasattr(context, 'auth_token')
    assert context.auth_token is not None
    assert len(context.auth_token) > 0


@then('the token should have an expiration time')
def step_impl(context):
    """Verify that the token has an expiration time."""
    assert hasattr(context, 'auth_response')
    assert context.auth_response.expires_in == 3600


@then('the auth error message should contain "{expected_text}"')
def step_impl(context, expected_text):
    """Verify that the error message contains the expected text."""
    assert context.error is not None
    assert expected_text in context.error