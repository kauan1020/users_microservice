from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List
from tech.core.domain.models import User
from tech.ports.repositories.user_repository import UserRepository
from tech.adapters.driven.infra.repositories.sql_alchemy_models import SQLAlchemyUser

class SQLAlchemyUserRepository(UserRepository):
    """
    SQLAlchemy implementation of the UserRepository interface.

    This repository provides methods for interacting with the User data model
    using SQLAlchemy ORM. It handles CRUD operations and ensures that User objects
    in the domain layer are transformed into SQLAlchemy objects for persistence.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a SQLAlchemy session.

        Args:
            session (Session): A SQLAlchemy session used for database operations.
                               The session should be managed by the caller (opened,
                               committed, and closed appropriately).
        """
        self.session = session

    def _to_domain_user(self, db_user: SQLAlchemyUser) -> User:
        """
        Convert a SQLAlchemyUser instance to a domain User instance.

        This method acts as a mapper between the SQLAlchemy model and the domain model.

        Args:
            db_user (SQLAlchemyUser): The SQLAlchemy model instance to convert.

        Returns:
            User: The domain model instance corresponding to the given SQLAlchemy model.
        """
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            password=db_user.password,
            cpf=db_user.cpf
        )

    def add(self, user: User) -> User:
        """
        Add a new user to the database.

        Converts the domain User object into a SQLAlchemyUser object and persists it
        in the database. Updates the `id` of the User object with the generated ID.

        Args:
            user (User): The domain User object to be added.

        Returns:
            User: The added User object with an updated `id` field.
        """
        db_user = SQLAlchemyUser(**user.__dict__)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        user.id = db_user.id
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Fetch a user by their unique ID.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            Optional[User]: The User object if found, or None if no user with the given ID exists.
        """
        db_user = self.session.scalar(select(SQLAlchemyUser).where(SQLAlchemyUser.id == user_id))
        return self._to_domain_user(db_user) if db_user else None

    def get_by_username_or_email_or_cpf(self, username: str, email: str, cpf: str) -> Optional[User]:
        """
        Fetch a user by username, email, or CPF.

        This method checks if a user with any of the given identifiers (username, email, or CPF)
        already exists in the database.

        Args:
            username (str): The username to search for.
            email (str): The email address to search for.
            cpf (str): The CPF (Cadastro de Pessoas Físicas, a Brazilian tax ID) to search for.

        Returns:
            Optional[User]: The User object if found, or None if no matching user exists.
        """
        db_user = self.session.scalar(
            select(SQLAlchemyUser).where(
                (SQLAlchemyUser.username == username) |
                (SQLAlchemyUser.email == email) |
                (SQLAlchemyUser.cpf == cpf)
            )
        )
        return self._to_domain_user(db_user) if db_user else None

    def list_users(self, limit: int, skip: int) -> List[User]:
        """
        Retrieve a list of users with pagination.

        This method returns a subset of users based on the limit and skip values,
        which can be used for pagination.

        Args:
            limit (int): The maximum number of users to retrieve.
            skip (int): The number of users to skip before starting to collect the results.

        Returns:
            List[User]: A list of User objects within the specified range.
        """
        db_users = self.session.scalars(select(SQLAlchemyUser).limit(limit).offset(skip)).all()
        return [self._to_domain_user(db_user) for db_user in db_users]

    def update(self, user: User) -> User:
        """
        Update an existing user's information in the database.

        Finds the user in the database by their ID and updates their fields with the
        values provided in the domain User object. Only fields present in the domain
        User are updated.

        Args:
            user (User): The domain User object with updated information.

        Returns:
            User: The updated User object.
        """
        db_user = self.session.scalar(select(SQLAlchemyUser).where(SQLAlchemyUser.id == user.id))
        if db_user:
            db_user.username = user.username
            db_user.password = user.password
            db_user.cpf = user.cpf
            db_user.email = user.email
            self.session.commit()
            self.session.refresh(db_user)
        return user

    def delete(self, user: User):
        """
        Delete a user from the database.

        Finds the user in the database by their ID and removes them from the database.
        If the user does not exist, no action is taken.

        Args:
            user (User): The domain User object representing the user to delete.
        """
        db_user = self.session.scalar(select(SQLAlchemyUser).where(SQLAlchemyUser.id == user.id))
        if db_user:
            self.session.delete(db_user)
            self.session.commit()
