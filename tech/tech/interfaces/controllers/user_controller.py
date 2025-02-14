from fastapi import HTTPException
from tech.use_cases.users.create_user_use_case import CreateUserUseCase
from tech.use_cases.users.list_users_use_case import ListUsersUseCase
from tech.use_cases.users.get_user_use_case import GetUserUseCase
from tech.use_cases.users.get_user_by_cpf_use_case import GetUserByCpfUseCase
from tech.use_cases.users.update_user_use_case import UpdateUserUseCase
from tech.use_cases.users.delete_user_use_case import DeleteUserUseCase
from tech.interfaces.presenters.user_presenter import UserPresenter
from tech.interfaces.schemas.user_schema import UserSchema

class UserController:
    """
    Controller responsible for managing user-related operations.
    """

    def __init__(
        self,
        create_user_use_case: CreateUserUseCase,
        list_users_use_case: ListUsersUseCase,
        get_user_use_case: GetUserUseCase,
        get_user_by_cpf_use_case: GetUserByCpfUseCase,
        update_user_use_case: UpdateUserUseCase,
        delete_user_use_case: DeleteUserUseCase
    ):
        """
        Initializes the UserController with the required use cases.

        Args:
            create_user_use_case (CreateUserUseCase): Use case for creating a user.
            list_users_use_case (ListUsersUseCase): Use case for listing users.
            get_user_use_case (GetUserUseCase): Use case for retrieving a user by ID.
            get_user_by_cpf_use_case (GetUserByCpfUseCase): Use case for retrieving a user by CPF.
            update_user_use_case (UpdateUserUseCase): Use case for updating a user.
            delete_user_use_case (DeleteUserUseCase): Use case for deleting a user.
        """
        self.create_user_use_case = create_user_use_case
        self.list_users_use_case = list_users_use_case
        self.get_user_use_case = get_user_use_case
        self.get_user_by_cpf_use_case = get_user_by_cpf_use_case
        self.update_user_use_case = update_user_use_case
        self.delete_user_use_case = delete_user_use_case

    def create_user(self, user_data: UserSchema) -> dict:
        """
        Creates a new user and returns a formatted response.

        Args:
            user_data (UserSchema): The data required to create a new user.

        Returns:
            dict: The formatted response containing user details.

        Raises:
            HTTPException: If a user with the same username, email, or CPF already exists.
        """
        try:
            user = self.create_user_use_case.execute(user_data)
            return UserPresenter.present_user(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def list_users(self, limit: int, skip: int) -> list:
        """
        Retrieves a paginated list of users.

        Args:
            limit (int): The maximum number of users to return.
            skip (int): The number of users to skip.

        Returns:
            list: A list of formatted user details.
        """
        users = self.list_users_use_case.execute(limit, skip)
        return UserPresenter.present_user_list(users)

    def get_user(self, user_id: int) -> dict:
        """
        Retrieves a user by their unique ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            dict: The formatted response containing user details.

        Raises:
            HTTPException: If no user is found with the given ID.
        """
        try:
            user = self.get_user_use_case.execute(user_id)
            return UserPresenter.present_user(user)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    def get_user_by_cpf(self, cpf: str) -> dict:
        """
        Retrieves a user by their CPF.

        Args:
            cpf (str): The CPF of the user.

        Returns:
            dict: The formatted response containing user details.

        Raises:
            HTTPException: If no user is found with the given CPF.
        """
        try:
            user = self.get_user_by_cpf_use_case.execute(cpf)
            return UserPresenter.present_user(user)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    def update_user(self, user_id: int, user_data: UserSchema) -> dict:
        """
        Updates a user's information.

        Args:
            user_id (int): The ID of the user to update.
            user_data (UserSchema): The updated user details.

        Returns:
            dict: The formatted response containing the updated user details.

        Raises:
            HTTPException: If the user is not found.
        """
        try:
            updated_user = self.update_user_use_case.execute(user_id, user_data)
            return UserPresenter.present_user(updated_user)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    def delete_user(self, user_id: int) -> dict:
        """
        Deletes a user by their unique ID.

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            dict: A success message confirming deletion.

        Raises:
            HTTPException: If the user is not found.
        """
        try:
            return self.delete_user_use_case.execute(user_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
