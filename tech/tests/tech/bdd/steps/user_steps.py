# tests/integration/steps/user_steps.py
from behave import given, when, then
from unittest.mock import Mock, patch
from fastapi import HTTPException
from tech.domain.entities.users import User
from tech.interfaces.schemas.user_schema import UserSchema


@given('the system has these existing users')
def step_impl(context):
    """Set up existing users in the system."""
    context.users = {}

    # Process the table data
    for row in context.table:
        user_id = int(row['id'])
        user = User(
            id=user_id,
            username=row['username'],
            email=row['email'],
            password="hashed_password",  # Placeholder for hashed password
            cpf=row['cpf']
        )
        context.users[user_id] = user


@when('I create a user with the following information')
def step_impl(context):
    """Simulate creating a new user."""
    # Get user data from the table
    row = context.table[0]
    user_data = UserSchema(
        username=row['username'],
        email=row['email'],
        password=row['password'],
        cpf=row['cpf']
    )

    # Mock the user repository
    with patch('tech.interfaces.gateways.user_gateway.SQLAlchemyUserRepository') as mock_repo_class:
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo

        # Configure mock behavior
        # Check if user with same CPF already exists
        existing_user = None
        for user in context.users.values():
            if user.cpf == row['cpf']:
                existing_user = user
                break

        mock_repo.get_by_username_or_email_or_cpf.return_value = existing_user

        # If no existing user, configure add method
        if not existing_user:
            new_user = User(
                id=len(context.users) + 1,
                username=row['username'],
                email=row['email'],
                password="hashed_password",  # Simulate hashed password
                cpf=row['cpf']
            )
            mock_repo.add.return_value = new_user

        # Create the gateway with the mocked repository
        from tech.interfaces.gateways.user_gateway import UserGateway
        user_gateway = UserGateway(Mock())  # Mock session

        # Create the use case
        from tech.use_cases.users.create_user_use_case import CreateUserUseCase
        create_user_use_case = CreateUserUseCase(user_gateway)

        # Create the controller
        from tech.interfaces.controllers.user_controller import UserController
        user_controller = UserController(
            create_user_use_case=create_user_use_case,
            list_users_use_case=Mock(),
            get_user_use_case=Mock(),
            get_user_by_cpf_use_case=Mock(),
            update_user_use_case=Mock(),
            delete_user_use_case=Mock()
        )

        # Execute the user creation
        try:
            context.response = user_controller.create_user(user_data)
            context.error = None
            context.operation_successful = True
        except HTTPException as e:
            context.error = e.detail
            context.status_code = e.status_code
            context.response = None
            context.operation_successful = False
        except ValueError as e:
            context.error = str(e)
            context.response = None
            context.operation_successful = False


@when('I request the user with ID {user_id}')
def step_impl(context, user_id):
    """Simulate requesting a user by ID."""
    user_id = int(user_id)

    # Mock the user repository
    with patch('tech.interfaces.gateways.user_gateway.SQLAlchemyUserRepository') as mock_repo_class:
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo

        # Configure mock to return user if exists
        mock_repo.get_by_id.return_value = context.users.get(user_id)

        # Create the gateway with the mocked repository
        from tech.interfaces.gateways.user_gateway import UserGateway
        user_gateway = UserGateway(Mock())  # Mock session

        # Create the use case
        from tech.use_cases.users.get_user_use_case import GetUserUseCase
        get_user_use_case = GetUserUseCase(user_gateway)

        # Create the controller
        from tech.interfaces.controllers.user_controller import UserController
        user_controller = UserController(
            create_user_use_case=Mock(),
            list_users_use_case=Mock(),
            get_user_use_case=get_user_use_case,
            get_user_by_cpf_use_case=Mock(),
            update_user_use_case=Mock(),
            delete_user_use_case=Mock()
        )

        # Execute the user retrieval
        try:
            context.response = user_controller.get_user(user_id)
            context.error = None
            context.operation_successful = True
        except HTTPException as e:
            context.error = e.detail
            context.status_code = e.status_code
            context.response = None
            context.operation_successful = False
        except ValueError as e:
            context.error = str(e)
            context.response = None
            context.operation_successful = False


@when('I request the user with CPF "{cpf}"')
def step_impl(context, cpf):
    """Simulate requesting a user by CPF."""
    # Mock the user repository
    with patch('tech.interfaces.gateways.user_gateway.SQLAlchemyUserRepository') as mock_repo_class:
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo

        # Find user with matching CPF
        found_user = None
        for user in context.users.values():
            if user.cpf == cpf:
                found_user = user
                break

        # Configure mock to return user if exists
        mock_repo.get_by_cpf.return_value = found_user

        # Create the gateway with the mocked repository
        from tech.interfaces.gateways.user_gateway import UserGateway
        user_gateway = UserGateway(Mock())  # Mock session

        # Create the use case
        from tech.use_cases.users.get_user_by_cpf_use_case import GetUserByCpfUseCase
        get_user_by_cpf_use_case = GetUserByCpfUseCase(user_gateway)

        # Create the controller
        from tech.interfaces.controllers.user_controller import UserController
        user_controller = UserController(
            create_user_use_case=Mock(),
            list_users_use_case=Mock(),
            get_user_use_case=Mock(),
            get_user_by_cpf_use_case=get_user_by_cpf_use_case,
            update_user_use_case=Mock(),
            delete_user_use_case=Mock()
        )

        # Execute the user retrieval
        try:
            context.response = user_controller.get_user_by_cpf(cpf)
            context.error = None
            context.operation_successful = True
        except HTTPException as e:
            context.error = e.detail
            context.status_code = e.status_code
            context.response = None
            context.operation_successful = False
        except ValueError as e:
            context.error = str(e)
            context.response = None
            context.operation_successful = False


@when('I update user with ID {user_id} with the following information')
def step_impl(context, user_id):
    """Simulate updating a user."""
    user_id = int(user_id)

    # Get update data from the table
    row = context.table[0]
    user_data = UserSchema(
        username=row['username'],
        email=row['email'],
        password=row['password'],
        cpf=row['cpf']
    )

    # Store the update data for later steps
    context.update_data = {
        'username': row['username'],
        'email': row['email'],
        'cpf': row['cpf']
    }

    # Mock the user repository
    with patch('tech.interfaces.gateways.user_gateway.SQLAlchemyUserRepository') as mock_repo_class:
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo

        # Configure mock behavior
        existing_user = context.users.get(user_id)
        mock_repo.get_by_id.return_value = existing_user

        # If user exists, configure update
        if existing_user:
            updated_user = User(
                id=user_id,
                username=row['username'],
                email=row['email'],
                password="new_hashed_password",  # Simulate new hashed password
                cpf=row['cpf']
            )
            mock_repo.update.return_value = updated_user

        # Create the gateway with the mocked repository
        from tech.interfaces.gateways.user_gateway import UserGateway
        user_gateway = UserGateway(Mock())  # Mock session

        # Create the use case
        from tech.use_cases.users.update_user_use_case import UpdateUserUseCase
        update_user_use_case = UpdateUserUseCase(user_gateway)

        # Create the controller
        from tech.interfaces.controllers.user_controller import UserController
        user_controller = UserController(
            create_user_use_case=Mock(),
            list_users_use_case=Mock(),
            get_user_use_case=Mock(),
            get_user_by_cpf_use_case=Mock(),
            update_user_use_case=update_user_use_case,
            delete_user_use_case=Mock()
        )

        # Execute the user update
        try:
            context.response = user_controller.update_user(user_id, user_data)
            context.error = None
            context.operation_successful = True

            # Update the user in context for subsequent steps
            if existing_user:
                context.users[user_id] = updated_user

        except HTTPException as e:
            context.error = e.detail
            context.status_code = e.status_code
            context.response = None
            context.operation_successful = False
        except ValueError as e:
            context.error = str(e)
            context.response = None
            context.operation_successful = False


@when('I delete the user with ID {user_id}')
def step_impl(context, user_id):
    """Simulate deleting a user."""
    user_id = int(user_id)

    # Mock the user repository
    with patch('tech.interfaces.gateways.user_gateway.SQLAlchemyUserRepository') as mock_repo_class:
        mock_repo = Mock()
        mock_repo_class.return_value = mock_repo

        # Configure mock behavior
        existing_user = context.users.get(user_id)
        mock_repo.get_by_id.return_value = existing_user

        # Create the gateway with the mocked repository
        from tech.interfaces.gateways.user_gateway import UserGateway
        user_gateway = UserGateway(Mock())  # Mock session

        # Create the use case
        from tech.use_cases.users.delete_user_use_case import DeleteUserUseCase
        delete_user_use_case = DeleteUserUseCase(user_gateway)

        # Create the controller
        from tech.interfaces.controllers.user_controller import UserController
        user_controller = UserController(
            create_user_use_case=Mock(),
            list_users_use_case=Mock(),
            get_user_use_case=Mock(),
            get_user_by_cpf_use_case=Mock(),
            update_user_use_case=Mock(),
            delete_user_use_case=delete_user_use_case
        )

        # Execute the user deletion
        try:
            context.response = user_controller.delete_user(user_id)
            context.error = None
            context.operation_successful = True

            # Remove the user from context if it exists
            if existing_user:
                del context.users[user_id]

        except HTTPException as e:
            context.error = e.detail
            context.status_code = e.status_code
            context.response = None
            context.operation_successful = False
        except ValueError as e:
            context.error = str(e)
            context.response = None
            context.operation_successful = False


@then('the user creation should be successful')
def step_impl(context):
    """Verify that user creation was successful."""
    assert context.operation_successful is True
    assert context.response is not None
    assert context.error is None


@then('the user creation should fail')
def step_impl(context):
    """Verify that user creation failed."""
    assert context.operation_successful is False
    assert context.response is None
    assert context.error is not None


@then('the request should be successful')
def step_impl(context):
    """Verify that the request was successful."""
    assert context.operation_successful is True
    assert context.response is not None
    assert context.error is None


@then('the request should fail')
def step_impl(context):
    """Verify that the request failed."""
    assert context.operation_successful is False
    assert context.response is None
    assert context.error is not None


@then('the user update should be successful')
def step_impl(context):
    """Verify that user update was successful."""
    assert context.operation_successful is True
    assert context.response is not None
    assert context.error is None


@then('the user deletion should be successful')
def step_impl(context):
    """Verify that user deletion was successful."""
    assert context.operation_successful is True
    assert context.response is not None
    assert context.error is None


@then('the response should include the user details')
def step_impl(context):
    """Verify that the response includes user details."""
    assert "id" in context.response
    assert "username" in context.response
    assert "email" in context.response


@then('the password should not be included in the response')
def step_impl(context):
    """Verify that the password is not included in the response."""
    assert "password" not in context.response


@then('the response should include user details for "{username}"')
def step_impl(context, username):
    """Verify that the response includes details for the specified user."""
    assert context.response["username"] == username


@then('the response should include the updated user details')
def step_impl(context):
    """Verify that the response includes the updated user details."""
    assert "username" in context.response
    assert "email" in context.response

    # Check that the response matches the update data
    if hasattr(context, 'update_data'):
        assert context.response["username"] == context.update_data['username']
        assert context.response["email"] == context.update_data['email']


@then('the user error message should contain "{expected_text}"')
def step_impl(context, expected_text):
    """Verify that the error message contains the expected text."""
    assert context.error is not None
    assert expected_text in context.error


@then('a confirmation message should be returned')
def step_impl(context):
    """Verify that a confirmation message was returned."""
    assert "message" in context.response
    assert "deleted" in context.response["message"].lower()