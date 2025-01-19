from tech.interfaces.repositories.user_repository import UserRepository

class GetUserUseCase(object):
    """
    Handles the retrieval of a user by their unique ID.

    This use case fetches a user from the repository using their ID
    and ensures that the user exists before returning the result.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the GetUserUseCase with the provided repository.

        Args:
            user_repository (UserRepository): The repository responsible for user-related data operations.
        """
        self.user_repository = user_repository

    def execute(self, user_id: int):
        """
        Executes the retrieval of a user by ID.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            User: The retrieved User entity.

        Raises:
            ValueError: If no user is found with the given ID.
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        return user
