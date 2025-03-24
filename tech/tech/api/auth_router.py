from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tech.infra.databases.database import get_session
from tech.interfaces.controllers.auth_controller import AuthController
from tech.use_cases.authenticate.authenticate_user_use_case import AuthenticateUserUseCase
from tech.interfaces.gateways.cognito_gateway import CognitoGateway
from tech.interfaces.schemas.auth_schema import AuthRequest, AuthResponse

router = APIRouter()


def get_auth_controller(session: Session = Depends(get_session)) -> AuthController:
    """Creates and returns an instance of the AuthController with its dependencies.

    This function follows the dependency injection pattern to create an AuthController
    with all its required dependencies. It creates a CognitoGateway and an
    AuthenticateUserUseCase, then injects them into the AuthController.

    Args:
        session (Session): The database session provided by FastAPI dependency injection.

    Returns:
        AuthController: A fully configured AuthController instance with all dependencies.
    """
    cognito_gateway = CognitoGateway()
    authenticate_user_use_case = AuthenticateUserUseCase(cognito_gateway)
    return AuthController(authenticate_user_use_case)


@router.post("/auth/login", response_model=AuthResponse)
def login(auth_request: AuthRequest, controller: AuthController = Depends(get_auth_controller)) -> AuthResponse:
    """Authenticates a user and returns an access token.

    This endpoint receives credentials (CPF and password) and attempts to authenticate
    the user against Amazon Cognito. If successful, it returns a token that can be used
    for subsequent authenticated requests.

    Args:
        auth_request (AuthRequest): The authentication request containing user credentials.
        controller (AuthController): The controller that handles the authentication logic.

    Returns:
        AuthResponse: Response containing the authentication token and expiration details.

    Raises:
        HTTPException: 401 Unauthorized if authentication fails for any reason.
    """
    try:
        return controller.authenticate(auth_request)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))