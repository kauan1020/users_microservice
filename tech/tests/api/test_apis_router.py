import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from http import HTTPStatus
from fastapi.testclient import TestClient
from tech.api.app import app
from tech.infra.databases.database import get_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from tech.infra.repositories.sql_alchemy_models import table_registry

@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    table_registry.metadata.create_all(engine)
    yield engine
    table_registry.metadata.drop_all(engine)

@pytest.fixture
def session(engine):
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()

@pytest.fixture
def client(session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

class DummyOrderController:
    def create_order(self, order):
        return self.checkout(order)
    def checkout(self, order: dict):
        return {"id": 1, "total_price": 100, "products": [{"id": 1}], "status": "CREATED"}
    def list_orders(self, limit: int, skip: int):
        return [{"id": 1, "total_price": 100, "products": [{"id": 1}], "status": "CREATED"}]
    def update_order_status(self, order_id: int, payload: dict):
        return {"message": "Order updated", "status": payload.get("status")}
    def delete_order(self, order_id: int):
        return {"message": "Order deleted"}

class DummyAuthController:
    def authenticate(self, auth_request: dict):
        if auth_request.get("cpf") == "valid":
            return {"access_token": "fake-token", "expires_in": 3600}
        raise Exception("Invalid credentials")

class DummyPaymentController:
    def create_payment(self, payment_data: dict):
        return {"payment_id": 1, "status": "created"}
    def get_payment_status(self, order_id: int):
        return {"order_id": order_id, "status": "paid"}
    def webhook_payment(self, order_id: int, status: str):
        return {"order_id": order_id, "status": status}

class DummyProductController:
    def list_all_products(self):
        return [{"id": 1, "name": "Product", "category": "electronics", "price": 100, "description": "A description"}]
    def list_products_by_category(self, category: str):
        return [{"id": 1, "name": "Product", "category": category, "price": 100, "description": "A description"}]
    def create_product(self, product: dict):
        return {"id": 1, **product}
    def update_product(self, product_id: int, product: dict):
        return {"id": product_id, **product}
    def delete_product(self, product_id: int):
        return {"message": "deleted"}

class DummyUserController:
    def create_user(self, user: dict):
        return {"id": 1, **user}
    def get_user(self, user_id: int):
        return {"id": user_id, "name": "User", "cpf": "12345678909", "email": "test@example.com"}
    def get_user_by_cpf(self, cpf: str):
        return {"cpf": cpf, "name": "User", "email": "test@example.com"}
    def list_users(self, limit: int, skip: int):
        return [{"id": i, "name": f"User{i}", "cpf": f"cpf{i}", "email": f"user{i}@example.com"}
                for i in range(skip+1, skip+limit+1)]
    def update_user(self, user_id: int, user: dict):
        return {"id": user_id, **user}
    def delete_user(self, user_id: int):
        return {"message": "deleted"}

class TestOrdersRouter:
    @pytest.fixture(autouse=True)
    def override_orders(self):
        from tech.api.orders_router import get_order_controller
        key = get_order_controller
        app.dependency_overrides[key] = lambda: DummyOrderController()
        yield
        app.dependency_overrides.pop(key, None)

    def test_should_create_order_with_success(self, client):
        payload = {"product_ids": [1]}
        response = client.post("/orders/checkout", json=payload)
        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert "id" in data
        assert "total_price" in data
        assert "products" in data
        assert "status" in data

    def test_should_list_orders_empty_with_success(self, client):
        response = client.get("/orders/")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert isinstance(data, list)

    def test_should_list_orders_with_data_with_success(self, client):
        create_response = client.post("/orders/checkout", json={"product_ids": [1]})
        assert create_response.status_code == HTTPStatus.CREATED
        list_response = client.get("/orders/")
        assert list_response.status_code == HTTPStatus.OK
        orders = list_response.json()
        assert len(orders) > 0
        assert "id" in orders[0]


    def test_should_delete_order_with_success(self, client):
        create_response = client.post("/orders/checkout", json={"product_ids": [1]})
        assert create_response.status_code == HTTPStatus.CREATED
        order_id = create_response.json()["id"]
        delete_response = client.delete(f"/orders/{order_id}")
        assert delete_response.status_code == HTTPStatus.OK
        data = delete_response.json()
        assert "message" in data

class TestAuthRouter:
    @pytest.fixture(autouse=True)
    def override_auth(self):
        from tech.api.auth_router import get_auth_controller
        key = get_auth_controller
        app.dependency_overrides[key] = lambda: DummyAuthController()
        yield
        app.dependency_overrides.pop(key, None)

class TestPaymentsRouter:
    @pytest.fixture(autouse=True)
    def override_payment(self):
        from tech.api.payments_router import get_payment_controller
        key = get_payment_controller
        app.dependency_overrides[key] = lambda: DummyPaymentController()
        yield
        app.dependency_overrides.pop(key, None)

    def test_webhook_payment(self, client):
        response = client.post("/payments/webhook?order_id=1&status=refunded")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data.get("status") == "refunded"

class TestProductsRouter:
    @pytest.fixture(autouse=True)
    def override_product(self):
        from tech.api.products_router import get_product_controller
        key = get_product_controller
        app.dependency_overrides[key] = lambda: DummyProductController()
        from tech.interfaces.middlewares.admin_auth_middleware import admin_required
        key_admin = admin_required
        app.dependency_overrides[key_admin] = lambda: True
        yield
        app.dependency_overrides.pop(key, None)
        app.dependency_overrides.pop(key_admin, None)

    def test_list_all_products(self, client):
        response = client.get("/products/")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert isinstance(data, list)

    def test_list_products_by_category(self, client):
        response = client.get("/products/electronics")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert isinstance(data, list)


    def test_delete_product(self, client):
        response = client.delete("/products/1")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "message" in data

class TestUsersRouter:
    @pytest.fixture(autouse=True)
    def override_user(self):
        from tech.api.users_router import get_user_controller
        key = get_user_controller
        app.dependency_overrides[key] = lambda: DummyUserController()
        yield
        app.dependency_overrides.pop(key, None)


    def test_get_user(self, client):
        response = client.get("/users/1")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data.get("id") == 1

    def test_get_user_by_cpf(self, client):
        response = client.get("/users/cpf/12345678909")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data.get("cpf") == "12345678909"

    def test_list_users(self, client):
        response = client.get("/users/?limit=5&skip=0")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert isinstance(data, list)


    def test_delete_user(self, client):
        response = client.delete("/users/1")
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert "message" in data
