import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from tech.adapters.driver.http.app import app
from tech.adapters.driven.infra.database import get_session
from tech.adapters.driven.infra.repositories.sql_alchemy_user_repository import SQLAlchemyUserRepository
from tech.adapters.driven.infra.repositories.sql_alchemy_product_repository import SQLAlchemyProductRepository
from tech.adapters.driven.infra.repositories.sql_alchemy_order_repository import SQLAlchemyOrderRepository
from tech.adapters.driven.infra.repositories.sql_alchemy_models import table_registry
from tech.core.domain.schemas import UserSchema, ProductSchema, OrderCreate, OrderStatusEnum
from tech.core.app.use_cases.users_use_cases import UserUseCase
from tech.core.app.use_cases.products_use_cases import ProductUseCase
from tech.core.app.use_cases.orders_use_cases import OrderUseCase
from tech.core.domain.models import Order, Products

@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())
        with _engine.begin():
            yield _engine

@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    table_registry.metadata.drop_all(engine)

@pytest.fixture
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
def user_use_case(session):
    user_repo = SQLAlchemyUserRepository(session)
    return UserUseCase(user_repo)

@pytest.fixture
def product_use_case(session):
    product_repo = SQLAlchemyProductRepository(session)
    return ProductUseCase(product_repo)

@pytest.fixture
def order_use_case(session, product_use_case):
    product_repo = SQLAlchemyProductRepository(session)
    order_repo = SQLAlchemyOrderRepository(session)
    return OrderUseCase(order_repo, product_repo)

@pytest.fixture
def user(user_use_case):
    user_data = UserSchema(
        username='Teste',
        email='teste@test.com',
        password='testtest',
        cpf='42190223489',
    )
    return user_use_case.create_user(user_data)

@pytest.fixture
def product(product_use_case):
    product_data = ProductSchema(
        name='Product Test',
        price=100.0,
        category='Lanche',
    )
    return product_use_case.create_product(product_data)

@pytest.fixture
def order(order_use_case, product):
    order_data = OrderCreate(product_ids=[product.id])
    created_order = order_use_case.create_order(order_data)

    order_instance = Order(
        id=created_order['id'],
        total_price=created_order['total_price'],
        status=OrderStatusEnum[created_order['status']],
        product_ids=order_data.product_ids
    )

    order_instance.products = [
        Products(id=prod['id'], name=prod['name'], price=prod['price'], category="Default Category")
        for prod in created_order['products']
    ]

    return order_instance



