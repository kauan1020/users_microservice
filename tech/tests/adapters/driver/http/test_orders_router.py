from http import HTTPStatus

from tech.core.domain.models import OrderStatus
from tests.adapters.driver.http.conftest import client, product


class TestOrders(object):
    def test_should_run_checkout_with_success(self, client, product):
        response = client.post('/orders/', json={'product_ids': [product.id]})

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data['total_price'] == product.price
        assert data['status'] == OrderStatus.RECEIVED.value
        assert len(data['products']) == 1
        assert data['products'][0]['name'] == product.name
        assert data['products'][0]['price'] == product.price

    def test_should_run_list_orders_with_success(self, client, order):
        response = client.get('/orders/')
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data['orders']) == 1
        assert data['orders'][0]['total_price'] == order.total_price
        assert data['orders'][0]['status'] == OrderStatus.RECEIVED.value

    def test_should_fail_due_create_order_with_invalid_product(self, client):
        response = client.post('/orders/', json={'product_ids': [999]})
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {'detail': 'Product with ID 999 not found'}

    def test_should_run_list_orders_with_empty_list(self, client):
        response = client.get('/orders/')
        assert response.status_code == 200
        assert response.json() == {'orders': []}

    def test_should_run_list_orders_with_order(self, client, order):
        response = client.get('/orders/')
        assert response.status_code == 200

        data = response.json()
        assert len(data['orders']) == 1
        order_data = data['orders'][0]

        assert order_data['id'] == order.id
        assert order_data['total_price'] == order.total_price
        assert order_data['status'] == OrderStatus.RECEIVED.value
        assert len(order_data['products']) == len(order.product_ids.split(','))

        for i, product_id in enumerate(order.product_ids.split(',')):
            product_id = int(product_id)
            assert order_data['products'][i]['id'] == product_id
