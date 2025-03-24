from pydantic import BaseModel


class AuthRequest(BaseModel):
    """Schema for authentication request payload.

    This model defines the structure of the authentication request
    that clients send to the /auth/login endpoint.

    Attributes:
        cpf (str): The user's CPF number used as the username for authentication.
        password (str): The user's password.
    """
    cpf: str
    password: str


class AuthResponse(BaseModel):
    """Schema for authentication response payload.

    This model defines the structure of the response sent back to clients
    after a successful authentication.

    Attributes:
        token (str): The JWT token that can be used for authenticated requests.
        expires_in (int): The token's time-to-live in seconds (default: 3600).
    """
    token: str
    expires_in: int

    class Config:
        """Configuration for the AuthResponse model.

        This configuration allows additional fields to be included in the
        response without causing validation errors.
        """
        extra = "allow"