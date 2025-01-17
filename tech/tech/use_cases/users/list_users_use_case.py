from tech.interfaces.repositories.user_repository import UserRepository

class ListUsersUseCase(object):
    """
    Handles the retrieval of users with pagination.

    This use case interacts with the repository to fetch a subset of users
    based on the provided pagination parameters.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the ListUsersUseCase with the provided repository.

        Args:
            user_repository (UserRepository): The repository responsible for user-related data operations.
        """
        self.user_repository = user_repository

    def execute(self, limit: int, skip: int) -> list:
        """
        Executes the listing of users with pagination.

        Args:
            limit (int): The maximum number of users to retrieve.
            skip (int): The number of users to skip before starting retrieval.

        Returns:
            list: A list of User entities.
        """
        return self.user_repository.list_users(limit, skip)
