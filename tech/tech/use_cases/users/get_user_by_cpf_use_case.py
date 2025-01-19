from tech.interfaces.repositories.user_repository import UserRepository

class GetUserByCpfUseCase(object):
    """
    Handles the retrieval of a user by their CPF.

    This use case fetches a user from the repository using their CPF
    and ensures that the user exists before returning the result.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the GetUserByCpfUseCase with the provided repository.

        Args:
            user_repository (UserRepository): The repository responsible for user-related data operations.
        """
        self.user_repository = user_repository

    def execute(self, cpf: str):
        """
        Executes the retrieval of a user by CPF.

        Args:
            cpf (str): The CPF of the user.

        Returns:
            User: The retrieved User entity.

        Raises:
            ValueError: If no user is found with the given CPF.
        """
        user = self.user_repository.get_by_cpf(cpf)
        if not user:
            raise ValueError('User not found')
        return user
