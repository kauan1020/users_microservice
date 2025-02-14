from sqlalchemy.orm import Session
from tech.domain.entities.users import User
from tech.interfaces.repositories.user_repository import UserRepository
from tech.infra.repositories.sql_alchemy_user_repository import SQLAlchemyUserRepository

class UserGateway(UserRepository):
    """
    Gateway that acts as an adapter between use cases and the database repository.
    """

    def __init__(self, session: Session):
        """
        Initializes the UserGateway with a database session.

        Args:
            session (Session): The SQLAlchemy session used for database transactions.
        """
        self.repository = SQLAlchemyUserRepository(session)

    def add(self, user: User) -> User:
        """
        Adds a new user to the repository.

        Args:
            user (User): The user entity to be added.

        Returns:
            User: The added user with an assigned ID.
        """
        return self.repository.add(user)

    def get_by_id(self, user_id: int) -> User:
        """
        Retrieves a user by its unique ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The user entity if found.
        """
        return self.repository.get_by_id(user_id)

    def get_by_cpf(self, cpf: str) -> User:
        """
        Retrieves a user by CPF.

        Args:
            cpf (str): The CPF of the user.

        Returns:
            User: The user entity if found.
        """
        return self.repository.get_by_cpf(cpf)

    def get_by_username_or_email_or_cpf(self, username: str, email: str, cpf: str) -> User:
        """
        Retrieves a user by username, email, or CPF.

        Args:
            username (str): The username to search for.
            email (str): The email to search for.
            cpf (str): The CPF to search for.

        Returns:
            User: The user entity if found.
        """
        return self.repository.get_by_username_or_email_or_cpf(username, email, cpf)

    def list_users(self, limit: int, skip: int):
        """
        Retrieves a paginated list of users.

        Args:
            limit (int): The number of users to retrieve.
            skip (int): The number of users to skip before retrieving.

        Returns:
            list: A list of user entities.
        """
        return self.repository.list_users(limit, skip)

    def update(self, user: User) -> User:
        """
        Updates an existing user's information.

        Args:
            user (User): The user entity with updated information.

        Returns:
            User: The updated user entity.
        """
        return self.repository.update(user)

    def delete(self, user: User):
        """
        Deletes a user from the repository.

        Args:
            user (User): The user entity to be deleted.
        """
        self.repository.delete(user)
