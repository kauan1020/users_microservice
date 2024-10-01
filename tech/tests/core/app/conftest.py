import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer


from tech.core.app.app import app
from tech.adapters.driven.infra.database import get_session
from tech.core.domain.models import User, Products, Order


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    from tech.core.domain.models import table_registry

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(
        username='Teste',
        email='teste@test.com',
        password='testtest',
        cpf='42190223489',
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture
def product(session):
    product = Products(
        name='Product Test',
        price=100.0,
        category='Lanche',
    )
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@pytest.fixture
def order(session, product):
    order = Order(
        total_price=product.price,
        product_ids=str(product.id),
        status='RECEIVED',
    )
    session.add(order)
    session.commit()
    session.refresh(order)
    return order
