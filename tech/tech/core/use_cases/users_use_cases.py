from tech.core.domain.models import User
from tech.core.domain.schemas import UserSchema
from tech.core.domain.security import get_password_hash, get_cpf_hash
from tech.ports.repositories.user_repository import UserRepository

class UserUseCase(object):
    """Use case layer for handling User-related business logic."""

    def __init__(self, user_repository: UserRepository):
        """Initialize UserUseCase with a repository."""
        self.user_repository = user_repository

    def create_user(self, user_data: UserSchema) -> User:
        """Create a new user."""
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
            cpf=get_cpf_hash(user_data.cpf),
            email=user_data.email,
        )

        return self.user_repository.add(new_user)

    def get_user(self, user_id: int) -> User:
        """Retrieve a user by their unique ID."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        return user

    def list_users(self, limit: int, skip: int):
        """List users with pagination."""
        return self.user_repository.list_users(limit, skip)

    def update_user(self, user_id: int, user_data: UserSchema) -> User:
        """Update a user's information."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('User not found')

        user.username = user_data.username
        user.password = get_password_hash(user_data.password)
        user.email = user_data.email
        user.cpf = get_cpf_hash(user_data.cpf)

        return self.user_repository.update(user)

    def delete_user(self, user_id: int) -> dict:
        """Delete a user by their unique ID."""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError('User not found')
        self.user_repository.delete(user)
        return {"message": "User deleted"}
