from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from tech.infra.databases.database import get_session
from tech.interfaces.gateways.user_gateway import UserGateway
from tech.interfaces.schemas.user_schema import UserSchema
from tech.use_cases.users.create_user_use_case import CreateUserUseCase
from tech.use_cases.users.list_users_use_case import ListUsersUseCase
from tech.use_cases.users.get_user_use_case import GetUserUseCase
from tech.use_cases.users.get_user_by_cpf_use_case import GetUserByCpfUseCase
from tech.use_cases.users.update_user_use_case import UpdateUserUseCase
from tech.use_cases.users.delete_user_use_case import DeleteUserUseCase
from tech.interfaces.controllers.user_controller import UserController

router = APIRouter()

def get_user_controller(session: Session = Depends(get_session)) -> UserController:
    """
    Creates and injects an instance of UserController with its required dependencies.

    Args:
        session (Session): The SQLAlchemy session for database operations.

    Returns:
        UserController: The controller instance containing all user-related use cases.
    """
    user_gateway = UserGateway(session)
    return UserController(
        create_user_use_case=CreateUserUseCase(user_gateway),
        list_users_use_case=ListUsersUseCase(user_gateway),
        get_user_use_case=GetUserUseCase(user_gateway),
        get_user_by_cpf_use_case=GetUserByCpfUseCase(user_gateway),
        update_user_use_case=UpdateUserUseCase(user_gateway),
        delete_user_use_case=DeleteUserUseCase(user_gateway),
    )

@router.post("/", status_code=201)
def create_user(user: UserSchema, controller: UserController = Depends(get_user_controller)):
    """
    API endpoint to create a new user.

    Args:
        user (UserSchema): The user's data required for registration.
        controller (UserController): The controller responsible for processing the request.

    Returns:
        dict: The created user's public information.
    """
    return controller.create_user(user)

@router.get("/{user_id}")
def get_user(user_id: int, controller: UserController = Depends(get_user_controller)):
    """
    API endpoint to retrieve a user by their unique ID.

    Args:
        user_id (int): The unique identifier of the user.
        controller (UserController): The controller responsible for processing the request.

    Returns:
        dict: The retrieved user's public information.

    Raises:
        HTTPException: If no user is found with the given ID.
    """
    return controller.get_user(user_id)

@router.get("/cpf/{cpf}")
def get_user_by_cpf(cpf: str, controller: UserController = Depends(get_user_controller)):
    """
    API endpoint to retrieve a user by their CPF.

    Args:
        cpf (str): The CPF (Cadastro de Pessoas Físicas) of the user.
        controller (UserController): The controller responsible for processing the request.

    Returns:
        dict: The retrieved user's public information.

    Raises:
        HTTPException: If no user is found with the given CPF.
    """
    return controller.get_user_by_cpf(cpf)

@router.get("/")
def list_users(
    limit: int = 10,
    skip: int = 0,
    controller: UserController = Depends(get_user_controller)
):
    """
    API endpoint to retrieve a list of users with pagination.

    Args:
        limit (int): The max number of users to return. Defaults to 10.
        skip (int): The number of users to skip before retrieving. Defaults to 0.
        controller (UserController): The controller responsible for processing the request.

    Returns:
        dict: A paginated list of users.
    """
    return controller.list_users(limit, skip)


@router.put("/{user_id}")
def update_user(user_id: int, user: UserSchema, controller: UserController = Depends(get_user_controller)):
    """
    API endpoint to update a user's information.

    Args:
        user_id (int): The unique identifier of the user.
        user (UserSchema): The updated user information.
        controller (UserController): The controller responsible for processing the request.

    Returns:
        dict: The updated user's public information.

    Raises:
        HTTPException: If the user is not found or if the update fails.
    """
    return controller.update_user(user_id, user)

@router.delete("/{user_id}")
def delete_user(user_id: int, controller: UserController = Depends(get_user_controller)):
    """
    API endpoint to delete a user by their unique ID.

    Args:
        user_id (int): The unique identifier of the user.
        controller (UserController): The controller responsible for processing the request.

    Returns:
        dict: A confirmation message indicating the user was deleted.

    Raises:
        HTTPException: If the user is not found.
    """
    return controller.delete_user(user_id)
