from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tech.adapters.driven.infra.database import get_session
from tech.core.domain.schemas import UserSchema, UserPublic, Message, UserList
from tech.core.use_cases.users_use_cases import UserUseCase
from tech.adapters.driven.infra.repositories.sql_alchemy_user_repository import SQLAlchemyUserRepository

router = APIRouter()

def get_user_use_case(session: Session = Depends(get_session)) -> UserUseCase:
    """Dependency injection for UserUseCase using the SQLAlchemyUserRepository.

    Args:
        session (Session): SQLAlchemy session for database operations.

    Returns:
        UserUseCase: The use case with a repository configured.
    """
    user_repository = SQLAlchemyUserRepository(session)
    return UserUseCase(user_repository)

@router.post('/', response_model=UserPublic, status_code=201)
def create_user(user: UserSchema, use_case: UserUseCase = Depends(get_user_use_case)):
    """Create a new user.

    Args:
        user (UserSchema): The user data for creating a new user.
        use_case (UserUseCase): The use case for user-related operations.

    Returns:
        UserPublic: The created user's public data.

    Raises:
        HTTPException: If a user with the same data already exists or any other validation error occurs.
    """
    try:
        created_user = use_case.create_user(user)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/', response_model=UserList)
def list_users(limit: int = 10, skip: int = 0, use_case: UserUseCase = Depends(get_user_use_case)):
    """List users with pagination.

    Args:
        limit (int, optional): The number of users to retrieve. Defaults to 10.
        skip (int, optional): The number of users to skip before retrieving. Defaults to 0.
        use_case (UserUseCase): The use case for user-related operations.

    Returns:
        UserList: A list of users.
    """
    users = use_case.list_users(limit, skip)
    return {'users': users}

@router.get('/{user_id}', response_model=UserPublic)
def get_user(user_id: int, use_case: UserUseCase = Depends(get_user_use_case)):
    """Retrieve a user by their unique ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        use_case (UserUseCase): The use case for user-related operations.

    Returns:
        UserPublic: The user's public data.

    Raises:
        HTTPException: If the user is not found.
    """
    try:
        return use_case.get_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, use_case: UserUseCase = Depends(get_user_use_case)):
    """Update a user's information.

    Args:
        user_id (int): The ID of the user to update.
        user (UserSchema): The updated user data.
        use_case (UserUseCase): The use case for user-related operations.

    Returns:
        UserPublic: The updated user's public data.

    Raises:
        HTTPException: If the user is not found or the update fails.
    """
    try:
        updated_user = use_case.update_user(user_id, user)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, use_case: UserUseCase = Depends(get_user_use_case)):
    """Delete a user by their unique ID.

    Args:
        user_id (int): The ID of the user to delete.
        use_case (UserUseCase): The use case for user-related operations.

    Returns:
        Message: A success message.

    Raises:
        HTTPException: If the user is not found.
    """
    try:
        return use_case.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
