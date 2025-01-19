from tech.interfaces.repositories.user_repository import UserRepository

class DeleteUserUseCase(object):
    """
    Handles the deletion of a user by their unique ID.

    This use case ensures that the user exists before deleting them
    from the repository.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the DeleteUserUseCase with the provided repository.

        Args:
            user_repository (UserRepository): The repository responsible for user-related data operations.
        """
        self.user_repository = user_repository

    def execute(self, user_id: int) -> dict:
        """
        Executes the deletion of a user.

        Args:
            user_id (int): The unique identifier of the user to delete.

        Returns:
            dict: A success message confirming the deletion.

        Raises:
            ValueError: If no user is found with the given ID.
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        self.user_repository.delete(user)
        return {"message": "User deleted"}
