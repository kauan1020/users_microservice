from http import HTTPStatus

from tech.core.domain.schemas import UserPublic

from tests.core.app.conftest import client, user


class TestUsers(object):
    def test_should_run_create_user_with_success(self, client):
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

    def test_shoud_fail_create_user_with_due_cpf_exists(self, client, user):
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

    def test_shoud_fail_create_user_with_due_invalid_cpf(self, client):
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

    def test_shoud_fail_create_user_with_due_username_exists(
        self, client, user
    ):
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

    def test_shoud_fail_create_user_with_due_email_exists(self, client, user):
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

    def test_should_run_read_users_with_success(self, client):
        response = client.get('/users')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'users': []}

    def test_should_run_read_users_with_users_with_success(self, client, user):
        user_schema = UserPublic.model_validate(user).model_dump()
        response = client.get('/users/')
        assert response.json() == {'users': [user_schema]}

    def test_should_update_user_with_success(self, client, user):
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

    def test_should_fail_update_due_invalid_user(self, client):
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

    def test_should_delete_user_with_success(self, client, user):
        response = client.delete('/users/1')

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'message': 'User deleted'}

    def test_should_fail_delete_user_due_invalid_user(self, client):
        response = client.delete('/users/224')

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'User not found'}
