from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from tech.app import app
from tech.database import get_session
from tech.models import User, table_registry, Products
from tech.schemas import UserPublic, ProductPublic


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


def test_should_run_create_user_with_success(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'password': 'password',
            'email': 'test@test.com',
            'cpf': '42190223489',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_shoud_fail_create_user_with_due_cpf_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'password': 'password',
            'email': 'test@test.com',
            'cpf': user.cpf,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'CPF already exists'}


def test_shoud_fail_create_user_with_due_invalid_cpf(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'password': 'password',
            'email': 'test@test.com',
            'cpf': '4234234234234234324',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'CPF must contain exactly 11 digits and be numeric.'
    }


def test_shoud_fail_create_user_with_due_username_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'password': 'password',
            'email': 'test@test.com',
            'cpf': '42190223489',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_shoud_fail_create_user_with_due_email_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'teste',
            'password': 'password',
            'email': user.email,
            'cpf': '42190223489',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_should_run_read_users_with_success(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_should_run_read_users_with_users_with_success(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_should_update_user_with_success(client, user):
    response = client.put(
        '/users/1',
        json={
            'password': '123',
            'username': 'testusername2',
            'email': 'test2@test.com',
            'id': 1,
            'cpf': '42190223489',
        },
    )

    assert response.json() == {
        'username': 'testusername2',
        'email': 'test2@test.com',
        'id': 1,
    }


def test_should_fail_update_due_invalid_user(client):
    response = client.put(
        '/users/224',
        json={
            'password': '123',
            'username': 'testusername2',
            'email': 'test2@test.com',
            'cpf': '42190223489',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_should_delete_user_with_success(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_should_fail_delete_user_due_invalid_user(client):
    response = client.delete('/users/224')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_should_run_create_product_with_success(client):
    response = client.post(
        '/products/',
        json={
            'name': 'Product 1',
            'price': 20.0,
            'category': 'Lanche',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'Product 1',
        'price': 20.0,
        'category': 'Lanche',
    }


def test_should_fail_create_product_with_duplicate_name(client, product):
    response = client.post(
        '/products/',
        json={
            'name': product.name,
            'price': 50.0,
            'category': 'Lanche',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Name already exists'}


def test_should_run_read_product_by_category_with_success(client, product):
    response = client.get(f'/products/{product.category}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'category': product.category,
        }
    ]


def test_should_update_product_with_success(client, product):
    response = client.put(
        f'/products/{product.id}',
        json={
            'name': 'Updated Product',
            'price': 200.0,
            'category': 'Lanche',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': product.id,
        'name': 'Updated Product',
        'price': 200.0,
        'category': 'Lanche',
    }


def test_should_fail_update_due_invalid_product(client):
    response = client.put(
        '/products/9999',
        json={
            'name': 'Updated Product',
            'price': 200.0,
            'category': 'Lanche',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Product not found'}


def test_should_delete_product_with_success(client, product):
    response = client.delete(f'/products/{product.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Product deleted successfully'}


def test_should_fail_delete_due_invalid_product(client):
    response = client.delete('/products/9999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Product not found'}
