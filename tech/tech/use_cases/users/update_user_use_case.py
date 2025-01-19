from tech.domain.security import get_password_hash
from tech.interfaces.repositories.user_repository import UserRepository
from tech.interfaces.schemas.user_schema import UserSchema

class UpdateUserUseCase(object):
    """
    Handles the updating of a user's information.

    This use case retrieves an existing user, validates their existence,
    and applies the updates provided in the input data.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the UpdateUserUseCase with the provided repository.

        Args:
            user_repository (UserRepository): The repository responsible for user-related data operations.
        """
        self.user_repository = user_repository

    def execute(self, user_id: int, user_data: UserSchema):
        """
        Executes the update of a user's information.

        Args:
            user_id (int): The unique identifier of the user to update.
            user_data (UserSchema): The updated user information.

        Returns:
            User: The updated User entity.

        Raises:
            ValueError: If no user is found with the given ID.
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('User not found')

        user.username = user_data.username
        user.password = get_password_hash(user_data.password)
        user.email = user_data.email
        user.cpf = user_data.cpf

        return self.user_repository.update(user)
