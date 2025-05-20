# tests/unit/api/test_user_router.py
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import FastAPI, HTTPException, Depends
from fastapi.testclient import TestClient
from tech.interfaces.controllers.user_controller import UserController
from tech.interfaces.schemas.user_schema import UserSchema

# Create a mock app with mock dependencies
app = FastAPI()
mock_controller = Mock(spec=UserController)

@app.post("/", status_code=201)
def create_user(user: UserSchema):
    return mock_controller.create_user(user)

@app.get("/{user_id}")
def get_user(user_id: int):
    return mock_controller.get_user(user_id)

@app.get("/cpf/{cpf}")
def get_user_by_cpf(cpf: str):
    return mock_controller.get_user_by_cpf(cpf)

@app.get("/")
def list_users(limit: int = 10, skip: int = 0):
    return mock_controller.list_users(limit, skip)

@app.put("/{user_id}")
def update_user(user_id: int, user: UserSchema):
    return mock_controller.update_user(user_id, user)

@app.delete("/{user_id}")
def delete_user(user_id: int):
    return mock_controller.delete_user(user_id)

client = TestClient(app)


class TestUserRouter:
    def setup_method(self):
        mock_controller.reset_mock()

    def test_create_user_endpoint(self):
        mock_controller.create_user.return_value = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com"
        }

        response = client.post(
            "/",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "Password123",
                "cpf": "12345678901"
            }
        )

        assert response.status_code == 201
        response_data = response.json()
        assert response_data["id"] == 1
        assert response_data["username"] == "testuser"
        assert response_data["email"] == "test@example.com"

        mock_controller.create_user.assert_called_once()

    def test_get_user_endpoint(self):
        mock_controller.get_user.return_value = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com"
        }

        response = client.get("/1")

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == 1
        assert response_data["username"] == "testuser"

        mock_controller.get_user.assert_called_once_with(1)

    def test_get_user_by_cpf_endpoint(self):
        mock_controller.get_user_by_cpf.return_value = {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com"
        }

        response = client.get("/cpf/12345678901")

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == 1

        mock_controller.get_user_by_cpf.assert_called_once_with("12345678901")

    def test_list_users_endpoint(self):
        mock_controller.list_users.return_value = [
            {"id": 1, "username": "user1", "email": "user1@example.com"},
            {"id": 2, "username": "user2", "email": "user2@example.com"}
        ]

        response = client.get("/")

        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 2
        assert response_data[0]["id"] == 1
        assert response_data[1]["id"] == 2

        mock_controller.list_users.assert_called_once_with(10, 0)

    def test_list_users_with_pagination(self):
        mock_controller.list_users.return_value = [
            {"id": 3, "username": "user3", "email": "user3@example.com"}
        ]

        response = client.get("/?limit=1&skip=2")

        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data) == 1
        assert response_data[0]["id"] == 3

        mock_controller.list_users.assert_called_once_with(1, 2)

    def test_update_user_endpoint(self):
        mock_controller.update_user.return_value = {
            "id": 1,
            "username": "updated_user",
            "email": "updated@example.com"
        }

        response = client.put(
            "/1",
            json={
                "username": "updated_user",
                "email": "updated@example.com",
                "password": "NewPassword123",
                "cpf": "12345678901"
            }
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == 1
        assert response_data["username"] == "updated_user"
        assert response_data["email"] == "updated@example.com"

        mock_controller.update_user.assert_called_once()

    def test_delete_user_endpoint(self):
        mock_controller.delete_user.return_value = {"message": "User deleted"}

        response = client.delete("/1")

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["message"] == "User deleted"

        mock_controller.delete_user.assert_called_once_with(1)

    def test_error_handling(self):
        mock_controller.get_user.side_effect = HTTPException(status_code=404, detail="User not found")

        response = client.get("/999")

        assert response.status_code == 404
        response_data = response.json()
        assert "User not found" in response_data["detail"]


# Dummy test to ensure original router imports work
def test_original_router_imports():
    from tech.api.users_router import router, get_user_controller
    assert router is not None
    assert callable(get_user_controller)