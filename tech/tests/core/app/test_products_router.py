import pytest
from http import HTTPStatus
from tests.core.app.conftest import client, product


class TestOrders(object):
    def test_should_run_create_product_with_success(self, client):
        response = client.post(
            '/products/',
            json={
                'name': 'Product 1',
                'price': 20.0,
                'category': 'Lanche',
            },
        )

        response_data = response.json()
        assert response.status_code == HTTPStatus.CREATED
        assert 'id' in response_data
        assert response_data['name'] == 'Product 1'
        assert response_data['price'] == 20.0
        assert response_data['category'] == 'Lanche'

    def test_should_fail_create_product_with_duplicate_name(
        self, client, product
    ):
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

    def test_should_run_read_product_by_category_with_success(
        self, client, product
    ):
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

    def test_should_update_product_with_success(self, client, product):
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

    def test_should_fail_update_due_invalid_product(self, client):
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

    def test_should_delete_product_with_success(self, client, product):
        response = client.delete(f'/products/{product.id}')

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'message': 'Product deleted successfully'}

    def test_should_fail_delete_due_invalid_product(self, client):
        response = client.delete('/products/9999')

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Product not found'}
