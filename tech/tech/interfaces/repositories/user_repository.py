from abc import ABC, abstractmethod
from typing import List, Optional
from tech.domain.entities.users import User


class UserRepository(ABC):
    """Interface for the user repository, defining the operations
    that the infrastructure should implement."""

    @abstractmethod
    def add(self, user: User) -> User:
        """Adds a new user to the repository.

        Args:
            user (User): The user entity to be added.

        Returns:
            User: The added user with an assigned ID.
        """
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieves a user by its ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            Optional[User]: The user entity if found, otherwise None.
        """
        pass

    @abstractmethod
    def get_by_username_or_email_or_cpf(self, username: str, email: str, cpf: str) -> Optional[User]:
        """Fetches a user by username, email, or CPF.

        Args:
            username (str): The user's username.
            email (str): The user's email.
            cpf (str): The user's CPF (Brazilian ID).

        Returns:
            Optional[User]: The matching user entity if found, otherwise None.
        """
        pass

    @abstractmethod
    def list_users(self, limit: int, skip: int) -> List[User]:
        """Retrieves a list of users with pagination.

        Args:
            limit (int): The number of users to retrieve.
            skip (int): The number of users to skip before retrieving.

        Returns:
            List[User]: A list of user entities.
        """
        pass

    def get_by_cpf(self, cpf: str) -> Optional[User]:
        """
        Fetch a user by their CPF.

        Args:
            cpf (str): The CPF (Cadastro de Pessoas Físicas, Brazilian tax ID) of the user.

        Returns:
            Optional[User]: The User object if found, or None if no user with the given CPF exists.
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Updates an existing user's information.

        Args:
            user (User): The user entity with updated information.

        Returns:
            User: The updated user entity.
        """
        pass

    @abstractmethod
    def delete(self, user: User) -> None:
        """Deletes a user from the repository.

        Args:
            user (User): The user entity to be deleted.
        """
        pass
