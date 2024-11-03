import pytest
from unittest.mock import Mock
from tech.core.app.use_cases.orders_use_cases import CreateOrderUseCase
from tech.core.domain.enums import OrderStatus


@pytest.fixture
def mock_product_repository():
    return Mock()


@pytest.fixture
def mock_order_repository():
    return Mock()


@pytest.fixture
def create_order_use_case(mock_product_repository, mock_order_repository):
    return CreateOrderUseCase(mock_product_repository, mock_order_repository)


def test_create_order_success(create_order_use_case, mock_product_repository, mock_order_repository):
    # Dados de exemplo
    product = Product(id=1, name="Test Product", price=100.0, category="Test Category")
    mock_product_repository.get_by_ids.return_value = [product]

    # Executa o caso de uso com uma lista de IDs de produtos
    order_data = {"product_ids": [product.id]}
    created_order = create_order_use_case.execute(order_data)

    # Verificações
    assert created_order.status == OrderStatus.RECEIVED
    assert created_order.total_price == product.price
    assert created_order.product_ids == [product.id]
    assert mock_order_repository.add.called_once_with(created_order)


def test_create_order_with_invalid_product_id(create_order_use_case, mock_product_repository):
    # Configura o repositório para retornar um produto inexistente
    mock_product_repository.get_by_ids.return_value = []

    # Executa o caso de uso com um ID de produto inválido
    order_data = {"product_ids": [999]}
    with pytest.raises(ValueError, match="Product with ID 999 not found"):
        create_order_use_case.execute(order_data)


def test_create_order_with_multiple_products(create_order_use_case, mock_product_repository, mock_order_repository):
    # Dados de exemplo para múltiplos produtos
    products = [
        Product(id=1, name="Product A", price=50.0, category="Category A"),
        Product(id=2, name="Product B", price=150.0, category="Category B")
    ]
    mock_product_repository.get_by_ids.return_value = products

    # Executa o caso de uso com vários IDs de produtos
    order_data = {"product_ids": [p.id for p in products]}
    created_order = create_order_use_case.execute(order_data)

    # Verificações
    assert created_order.status == OrderStatus.RECEIVED
    assert created_order.total_price == sum(p.price for p in products)
    assert created_order.product_ids == [p.id for p in products]
    assert mock_order_repository.add.called_once_with(created_order)
