from http import HTTPStatus
from tech.core.domain.schemas import UserPublic
from tests.adapters.driver.http.conftest import client, user

class TestUsers(object):

    @staticmethod
    def create_user(client, user_data):
        """Helper function to create a user via the API."""
        return client.post("/users/", json=user_data)

    @staticmethod
    def get_user(client, user_id=None):
        """Helper function to get user(s) via the API."""
        url = f"/users/{user_id}" if user_id else "/users/"
        return client.get(url)

    @staticmethod
    def update_user(client, user_id, update_data):
        """Helper function to update a user via the API."""
        return client.put(f"/users/{user_id}", json=update_data)

    @staticmethod
    def delete_user(client, user_id):
        """Helper function to delete a user via the API."""
        return client.delete(f"/users/{user_id}")

    def test_should_fail_create_user_due_invalid_cpf(self, client):
        response = self.create_user(
            client,
            {
                "username": "testusername2",
                "password": "password",
                "email": "test@test.com",
                "cpf": "4234234234234234324",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "detail": "CPF must contain exactly 11 digits and be numeric."
        }

    def test_should_fail_create_user_due_username_exists(self, client, user):
        response = self.create_user(
            client,
            {
                "username": user.username,
                "password": "password",
                "email": "test@test.com",
                "cpf": "10022223334",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"detail": "User already exists"}

    def test_should_fail_create_user_due_email_exists(self, client, user):
        response = self.create_user(
            client,
            {
                "username": "teste",
                "password": "password",
                "email": user.email,
                "cpf": "10022223334",
            },
        )

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"detail": "User already exists"}

    def test_should_run_read_users_with_success(self, client):
        response = self.get_user(client)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"users": []}

    def test_should_run_read_users_with_users_with_success(self, client, user):
        user_schema = UserPublic.model_validate(user).model_dump()
        response = self.get_user(client)
        assert response.json() == {"users": [user_schema]}

    def test_should_update_user_with_success(self, client, user):
        update_data = {
            "password": "123",
            "username": "testusername2",
            "email": "test2@test.com",
            "id": user.id,
            "cpf": "42190223489",
        }
        response = self.update_user(client, user.id, update_data)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "username": "testusername2",
            "email": "test2@test.com",
            "id": user.id,
        }

    def test_should_fail_update_due_invalid_user(self, client):
        response = self.update_user(
            client,
            224,
            {
                "password": "123",
                "username": "testusername2",
                "email": "test2@test.com",
                "cpf": "42190223489",
            },
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {"detail": "User not found"}

    def test_should_delete_user_with_success(self, client, user):
        response = self.delete_user(client, user.id)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"message": "User deleted"}

    def test_should_fail_delete_user_due_invalid_user(self, client):
        response = self.delete_user(client, 224)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {"detail": "User not found"}
