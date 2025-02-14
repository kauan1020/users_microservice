class UserPresenter:
    """
    Handles the formatting of user-related responses.

    This class provides methods to transform user entities into a structured response format
    that is suitable for API responses.
    """

    @staticmethod
    def present_user(user: object) -> dict:
        """
        Formats a single user response.

        Args:
            user (object): The user entity to format.

        Returns:
            dict: A dictionary containing the formatted user details.
        """
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "cpf": user.cpf
        }

    @staticmethod
    def present_user_list(users: list) -> list:
        """
        Formats a list of users.

        Args:
            users (list): A list of user entities.

        Returns:
            list: A list of dictionaries containing formatted user details.
        """
        return [UserPresenter.present_user(user) for user in users]
