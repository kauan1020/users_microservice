from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from tech.use_cases.products.verify_token_use_case import VerifyTokenUseCase
from tech.interfaces.gateways.cognito_gateway import CognitoGateway

security = HTTPBearer()


def admin_required(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Middleware that ensures the request comes from an admin user.

    This middleware extracts the token from the authorization header,
    verifies it with Amazon Cognito, and checks if the user belongs
    to the admin group. If any of these checks fail, the appropriate
    HTTP exception is raised.

    Args:
        credentials (HTTPAuthorizationCredentials): The authorization credentials
            extracted from the request header. Contains the bearer token.

    Returns:
        bool: True if the user is an admin, allowing the request to proceed.

    Raises:
        HTTPException:
            401 Unauthorized - If authentication fails (invalid/expired token)
            403 Forbidden - If the user is authenticated but not an admin
    """
    print("Admin authentication middleware invoked")

    if not credentials:
        print("No credentials provided")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials not provided"
        )

    token = credentials.credentials
    print(f"Token received: {token[:20]}...")

    cognito_gateway = CognitoGateway()
    verify_token_use_case = VerifyTokenUseCase(cognito_gateway)

    try:
        if not token or not isinstance(token, str):
            raise ValueError("Token must be a non-empty string")

        print("Verifying token...")
        user_data = verify_token_use_case.execute(token)

        print(f"Token successfully verified: {user_data}")

        if not user_data.get("is_admin", False):
            print(f"User is not an admin: {user_data.get('username')}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions. Admin access required."
            )

        print(f"Admin authentication successful for: {user_data.get('username')}")
        return True

    except ValueError as e:
        print(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}"
        )
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}"
        )