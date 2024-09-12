from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from tech.app import app
from tech.database import get_session
from tech.models import User, table_registry
from tech.schemas import UserPublic


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
    user = User(username='Teste', email='teste@test.com', password='testtest')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def test_should_run_create_user_with_success(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'password': 'password',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_shoud_fail_create_user_with_due_username_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'password': 'password',
            'email': 'test@test.com',
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


def test_shoud_update_user_with_success(client, user):
    response = client.put(
        '/users/1',
        json={
            'password': '123',
            'username': 'testusername2',
            'email': 'test2@test.com',
            'id': 1,
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
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_should_fail_delete_user_due_invalid_user(client):
    response = client.delete('/users/224')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
