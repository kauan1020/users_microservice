from tech.domain.entities.users import User
from tech.interfaces.schemas.user_schema import UserSchema
from tech.domain.security import get_password_hash
from tech.interfaces.repositories.user_repository import UserRepository

class CreateUserUseCase(object):
    """
    Handles the creation of a new user.

    This use case validates the provided user data, checks for existing users
    with the same username, email, or CPF, and hashes the user's password
    before persisting the user in the repository.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the CreateUserUseCase with the provided repository.

        Args:
            user_repository (UserRepository): The repository responsible for user-related data operations.
        """
        self.user_repository = user_repository

    def execute(self, user_data: UserSchema) -> User:
        """
        Executes the creation of a new user.

        Args:
            user_data (UserSchema): The data required to create a new user.

        Returns:
            User: The created User entity.

        Raises:
            ValueError: If the CPF is invalid or if a user with the same username, email, or CPF already exists.
        """
        if len(user_data.cpf) != 11 or not user_data.cpf.isdigit():
            raise ValueError('CPF must contain exactly 11 digits and be numeric.')

        existing_user = self.user_repository.get_by_username_or_email_or_cpf(
            user_data.username, user_data.email, user_data.cpf
        )

        if existing_user:
            raise ValueError('User already exists')

        new_user = User(
            username=user_data.username,
            password=get_password_hash(user_data.password),
            cpf=user_data.cpf,
            email=user_data.email,
        )

        return self.user_repository.add(new_user)
