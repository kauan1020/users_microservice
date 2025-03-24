from tech.use_cases.authenticate.authenticate_user_use_case import AuthenticateUserUseCase
from tech.interfaces.schemas.auth_schema import AuthRequest, AuthResponse

class AuthController:
    def __init__(self, authenticate_user_use_case: AuthenticateUserUseCase):
        self.authenticate_user_use_case = authenticate_user_use_case

    def authenticate(self, auth_request: AuthRequest) -> AuthResponse:
        return self.authenticate_user_use_case.execute(auth_request)
