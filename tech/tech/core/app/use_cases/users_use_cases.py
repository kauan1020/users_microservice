from tech.core.domain.models import User
from tech.core.domain.schemas import UserSchema
from tech.core.domain.security import get_password_hash
from tech.core.app.repositories.user_repository import UserRepository

class UserUseCase:
    """Handles business logic related to user management, acting as an intermediary
    between the application and the data layer for User entities.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initializes the UserUseCase with a user repository to interact with the data layer.

        Args:
            user_repository (UserRepository): A repository instance for user-related operations.
        """
        self.user_repository = user_repository

    def create_user(self, user_data: UserSchema) -> User:
        """
        Creates a new user with the provided data.

        This method performs basic validation on the CPF, checks for existing users
        with the same username, email, or CPF, and hashes the password before saving.

        Args:
            user_data (UserSchema): Data schema containing user information.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If the CPF is invalid or if a user with the same username, email,
                        or CPF already exists.
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

    def get_user(self, user_id: int) -> User:
        """
        Retrieves a user by their unique ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            User: The retrieved User object.

        Raises:
            ValueError: If no user is found with the given ID.
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        return user

    def list_users(self, limit: int, skip: int) -> list:
        """
        Lists users with pagination.

        Args:
            limit (int): The maximum number of users to retrieve.
            skip (int): The number of users to skip before retrieving.

        Returns:
            list: A list of User objects within the specified range.
        """
        return self.user_repository.list_users(limit, skip)

    def get_user_by_cpf(self, cpf: str) -> User:
        """
        Retrieves a user by their CPF.

        Args:
            cpf (str): The CPF of the user to retrieve.

        Returns:
            User: The retrieved User object.

        Raises:
            ValueError: If no user is found with the given CPF.
        """
        user = self.user_repository.get_by_cpf(cpf)
        if not user:
            raise ValueError('User not found')
        return user

    def update_user(self, user_id: int, user_data: UserSchema) -> User:
        """
        Updates a user's information.

        This method hashes the password before updating the record.

        Args:
            user_id (int): The ID of the user to update.
            user_data (UserSchema): Data schema containing updated user information.

        Returns:
            User: The updated User object.

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

    def delete_user(self, user_id: int) -> dict:
        """
        Deletes a user by their unique ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            dict: A message confirming successful deletion.

        Raises:
            ValueError: If no user is found with the given ID.
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        self.user_repository.delete(user)
        return {"message": "User deleted"}
