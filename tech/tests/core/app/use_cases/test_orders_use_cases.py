import pytest
from unittest.mock import Mock
from tech.domain import Order, Products, OrderStatus
from tech.interfaces.schemas import OrderCreate, OrderStatusEnum
from tech.use_cases.orders_use_cases import OrderUseCase


@pytest.fixture
def mock_order_repository():
    return Mock()


@pytest.fixture
def mock_product_repository():
    return Mock()


@pytest.fixture
def order_use_case(mock_order_repository, mock_product_repository):
    return OrderUseCase(mock_order_repository, mock_product_repository)


class TestOrderUseCase(object):

    def test_create_order_success(self, order_use_case, mock_product_repository, mock_order_repository):
        product = Products(id=1, name="Product Test", price=100.0, category="Test Category")
        mock_product_repository.get_by_id.return_value = product

        order_data = OrderCreate(product_ids=[1])
        new_order = Order(id=1, total_price=100.0, product_ids="1", status=OrderStatus.RECEIVED)
        mock_order_repository.add.return_value = new_order

        result = order_use_case.create_order(order_data)

        assert result['id'] == 1
        assert result['total_price'] == 100.0
        assert result['status'] == OrderStatusEnum.RECEIVED
        assert result['products'][0]['name'] == "Product Test"
        mock_product_repository.get_by_id.assert_called_once_with(1)
        mock_order_repository.add.assert_called_once()

    def test_create_order_with_invalid_product_id(self, order_use_case, mock_product_repository):
        mock_product_repository.get_by_id.return_value = None
        order_data = OrderCreate(product_ids=[999])

        with pytest.raises(ValueError, match="Product with ID 999 not found"):
            order_use_case.create_order(order_data)

    def test_list_orders_success(self, order_use_case, mock_order_repository, mock_product_repository):
        product = Products(id=1, name="Product Test", price=100.0, category="Test Category")
        order = Order(id=1, total_price=100.0, product_ids="1", status=OrderStatus.RECEIVED)
        mock_order_repository.list_orders.return_value = [order]
        mock_product_repository.get_by_id.return_value = product

        result = order_use_case.list_orders(limit=10, skip=0)

        assert len(result) == 1
        assert result[0]['id'] == order.id
        assert result[0]['total_price'] == order.total_price
        assert result[0]['status'] == OrderStatusEnum.RECEIVED
        assert result[0]['products'][0]['name'] == "Product Test"

    def test_update_order_status_success(self, order_use_case, mock_order_repository):
        order = Order(id=1, total_price=100.0, product_ids="1", status=OrderStatus.RECEIVED)
        mock_order_repository.get_by_id.return_value = order

        result = order_use_case.update_order_status(order_id=1, status=OrderStatusEnum.FINISHED)

        assert result == {"message": "Order status updated successfully"}
        assert order.status == OrderStatus.FINISHED
        mock_order_repository.update.assert_called_once_with(order)

    def test_update_order_status_order_not_found(self, order_use_case, mock_order_repository):
        mock_order_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Order not found"):
            order_use_case.update_order_status(order_id=1, status=OrderStatusEnum.FINISHED)

    def test_delete_order_success(self, order_use_case, mock_order_repository):
        order = Order(id=1, total_price=100.0, product_ids="1", status=OrderStatus.RECEIVED)
        mock_order_repository.get_by_id.return_value = order

        result = order_use_case.delete_order(order_id=1)

        assert result == {'message': 'Order deleted successfully'}
        mock_order_repository.delete.assert_called_once_with(order)

    def test_delete_order_not_found(self, order_use_case, mock_order_repository):
        mock_order_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Order not found"):
            order_use_case.delete_order(order_id=1)
