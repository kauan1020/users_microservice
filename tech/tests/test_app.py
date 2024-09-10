from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from tech.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_create_user(client):
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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'testusername',
                'email': 'test@test.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
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


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_should_fail_delete_user_due_invalid_user(client):
    response = client.delete('/users/224')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
