from tech.interfaces.schemas.auth_schema import AuthRequest, AuthResponse
from tech.interfaces.gateways.cognito_gateway import CognitoGateway


class AuthenticateUserUseCase:
    """Use case for authenticating users against Amazon Cognito.

    This class implements the business logic for user authentication
    following the Clean Architecture pattern. It depends on the
    CognitoGateway to handle the actual communication with AWS Cognito.
    """

    def __init__(self, cognito_gateway: CognitoGateway):
        """Initializes the use case with required dependencies.

        Args:
            cognito_gateway (CognitoGateway): The gateway for Cognito operations.
        """
        self.cognito_gateway = cognito_gateway

    def execute(self, auth_request: AuthRequest) -> AuthResponse:
        """Executes the authentication process.

        Attempts to authenticate the user with the provided credentials
        using the Cognito gateway, and formats the response appropriately.

        Args:
            auth_request (AuthRequest): The authentication request containing
                the user's CPF and password.

        Returns:
            AuthResponse: The authentication response containing the token
                and its expiration time.

        Raises:
            ValueError: If authentication fails due to invalid credentials,
                       user not found, or other authentication errors.
        """
        try:
            auth_result = self.cognito_gateway.authenticate(
                auth_request.cpf,
                auth_request.password
            )

            if not auth_result:
                raise ValueError("Authentication failed: empty response")

            token = auth_result.get("IdToken", "")

            return AuthResponse(
                token=token,
                expires_in=auth_result.get("ExpiresIn", 3600)
            )

        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Authentication failed: {str(e)}")