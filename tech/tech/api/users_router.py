from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tech.infra.databases.database import get_session
from tech.interfaces.schemas.user_schema import UserSchema, UserPublic, UserList
from tech.interfaces.schemas.message_schema import Message
from tech.use_cases.users.create_user_use_case import CreateUserUseCase
from tech.use_cases.users.list_users_use_case import ListUsersUseCase
from tech.use_cases.users.get_user_use_case import GetUserUseCase
from tech.use_cases.users.get_user_by_cpf_use_case import GetUserByCpfUseCase
from tech.use_cases.users.update_user_use_case import UpdateUserUseCase
from tech.use_cases.users.delete_user_use_case import DeleteUserUseCase
from tech.infra.repositories.sql_alchemy_user_repository import SQLAlchemyUserRepository

router = APIRouter()

def get_user_repository(session: Session = Depends(get_session)) -> SQLAlchemyUserRepository:
    """
    Provides an instance of SQLAlchemyUserRepository for dependency injection.

    Args:
        session (Session): A SQLAlchemy session for database operations.

    Returns:
        SQLAlchemyUserRepository: A repository instance for user-related operations.
    """
    return SQLAlchemyUserRepository(session)

@router.post('/', response_model=UserPublic, status_code=201)
def create_user(
    user: UserSchema,
    repository: SQLAlchemyUserRepository = Depends(get_user_repository)
):
    """
    Creates a new user in the system.

    Args:
        user (UserSchema): The data required to create the new user.
        repository (SQLAlchemyUserRepository): The user repository for data operations.

    Returns:
        UserPublic: The created user's public information.

    Raises:
        HTTPException: If the CPF is invalid or if a user with the same username, email, or CPF already exists.
    """
    try:
        use_case = CreateUserUseCase(repository)
        created_user = use_case.execute(user)
        return created_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/', response_model=UserList)
def list_users(
    limit: int = 10,
    skip: int = 0,
    repository: SQLAlchemyUserRepository = Depends(get_user_repository)
):
    """
    Retrieves a paginated list of users.

    Args:
        limit (int): The maximum number of users to return. Defaults to 10.
        skip (int): The number of users to skip. Defaults to 0.
        repository (SQLAlchemyUserRepository): The user repository for data operations.

    Returns:
        UserList: A list of users with their public information.
    """
    use_case = ListUsersUseCase(repository)
    users = use_case.execute(limit, skip)
    return {'users': users}

@router.get('/{user_id}', response_model=UserPublic)
def get_user(
    user_id: int,
    repository: SQLAlchemyUserRepository = Depends(get_user_repository)
):
    """
    Retrieves a user by their unique ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        repository (SQLAlchemyUserRepository): The user repository for data operations.

    Returns:
        UserPublic: The user's public information.

    Raises:
        HTTPException: If no user is found with the given ID.
    """
    try:
        use_case = GetUserUseCase(repository)
        return use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get('/cpf/{cpf}', response_model=UserPublic)
def get_user_by_cpf(
    cpf: str,
    repository: SQLAlchemyUserRepository = Depends(get_user_repository)
):
    """
    Retrieves a user by their CPF.

    Args:
        cpf (str): The CPF of the user to retrieve.
        repository (SQLAlchemyUserRepository): The user repository for data operations.

    Returns:
        UserPublic: The user's public information.

    Raises:
        HTTPException: If no user is found with the given CPF.
    """
    try:
        use_case = GetUserByCpfUseCase(repository)
        return use_case.execute(cpf)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    repository: SQLAlchemyUserRepository = Depends(get_user_repository)
):
    """
    Updates a user's information.

    Args:
        user_id (int): The ID of the user to update.
        user (UserSchema): The updated user information.
        repository (SQLAlchemyUserRepository): The user repository for data operations.

    Returns:
        UserPublic: The updated user's public information.

    Raises:
        HTTPException: If no user is found with the given ID or if the update fails.
    """
    try:
        use_case = UpdateUserUseCase(repository)
        updated_user = use_case.execute(user_id, user)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    repository: SQLAlchemyUserRepository = Depends(get_user_repository)
):
    """
    Deletes a user by their unique ID.

    Args:
        user_id (int): The ID of the user to delete.
        repository (SQLAlchemyUserRepository): The user repository for data operations.

    Returns:
        Message: A confirmation message indicating the user was deleted.

    Raises:
        HTTPException: If no user is found with the given ID.
    """
    try:
        use_case = DeleteUserUseCase(repository)
        return use_case.execute(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
