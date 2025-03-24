from tech.interfaces.gateways.cognito_gateway import CognitoGateway


class VerifyTokenUseCase:
    """
    Use case for verifying a JWT token and extracting user information.
    """

    def __init__(self, cognito_gateway: CognitoGateway):
        """
        Initialize the use case with the required gateway.

        Args:
            cognito_gateway (CognitoGateway): The gateway for Cognito operations.
        """
        self.cognito_gateway = cognito_gateway

    def execute(self, token: str) -> dict:
        """
        Verify the provided token and return user information.

        Args:
            token (str): The JWT token to verify.

        Returns:
            dict: User information, including admin status.

        Raises:
            Exception: If token verification fails or user is not found.
        """
        try:
            print(f"Attempting to verify token: {token[:10]}...")
            user_data = self.cognito_gateway.verify_token(token)
            print(f"Token verified successfully, user data: {user_data}")
            return user_data
        except Exception as e:
            print(f"Token verification failed: {str(e)}")
            raise