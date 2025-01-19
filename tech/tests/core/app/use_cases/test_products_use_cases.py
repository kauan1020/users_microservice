import pytest
from unittest.mock import Mock
from tech.domain import Products
from tech.interfaces.schemas import ProductSchema
from tech.use_cases import ProductUseCase


@pytest.fixture
def mock_product_repository():
    return Mock()


@pytest.fixture
def product_use_case(mock_product_repository):
    return ProductUseCase(mock_product_repository)


class TestProductUseCase(object):
    def test_create_product_success(self, product_use_case, mock_product_repository):
        product_data = ProductSchema(name="Test Product", price=100.0, category="Lanche")
        mock_product_repository.get_by_name.return_value = None
        new_product = Products(id=1, name="Test Product", price=100.0, category="Lanche")
        mock_product_repository.add.return_value = new_product

        result = product_use_case.create_product(product_data)

        assert result.id == 1
        assert result.name == "Test Product"
        assert result.price == 100.0
        assert result.category == "Lanche"
        mock_product_repository.get_by_name.assert_called_once_with("Test Product")
        mock_product_repository.add.assert_called_once()

    def test_create_product_already_exists(self, product_use_case, mock_product_repository):
        product_data = ProductSchema(name="Test Product", price=100.0, category="Lanche")
        existing_product = Products(id=1, name="Test Product", price=100.0, category="Lanche")
        mock_product_repository.get_by_name.return_value = existing_product

        with pytest.raises(ValueError, match="Product already exists"):
            product_use_case.create_product(product_data)

    def test_get_product_success(self, product_use_case, mock_product_repository):
        product = Products(id=1, name="Test Product", price=100.0, category="Lanche")
        mock_product_repository.get_by_id.return_value = product

        result = product_use_case.get_product(product_id=1)

        assert result.id == 1
        assert result.name == "Test Product"
        assert result.price == 100.0
        assert result.category == "Lanche"
        mock_product_repository.get_by_id.assert_called_once_with(1)

    def test_get_product_not_found(self, product_use_case, mock_product_repository):
        mock_product_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Product not found"):
            product_use_case.get_product(product_id=999)

    def test_list_products_by_category(self, product_use_case, mock_product_repository):
        products = [
            Products(id=1, name="Product 1", price=50.0, category="Lanche"),
            Products(id=2, name="Product 2", price=75.0, category="Lanche"),
        ]
        mock_product_repository.list_by_category.return_value = products

        result = product_use_case.list_products_by_category(category="Lanche")

        assert len(result) == 2
        assert result[0].name == "Product 1"
        assert result[1].name == "Product 2"
        mock_product_repository.list_by_category.assert_called_once_with("Lanche")

    def test_list_all_products(self, product_use_case, mock_product_repository):
        products = [
            Products(id=1, name="Product 1", price=50.0, category="Lanche"),
            Products(id=2, name="Product 2", price=75.0, category="Bebida"),
        ]
        mock_product_repository.list_all_products.return_value = products

        result = product_use_case.list_all_products()

        assert len(result) == 2
        assert result[0].name == "Product 1"
        assert result[1].name == "Product 2"
        mock_product_repository.list_all_products.assert_called_once()

    def test_update_product_success(self, product_use_case, mock_product_repository):
        product = Products(id=1, name="Old Product", price=80.0, category="Lanche")
        mock_product_repository.get_by_id.return_value = product
        updated_data = ProductSchema(name="Updated Product", price=90.0, category="Bebida")
        updated_product = Products(id=1, name="Updated Product", price=90.0, category="Bebida")
        mock_product_repository.update.return_value = updated_product

        result = product_use_case.update_product(product_id=1, product_data=updated_data)

        assert result.name == "Updated Product"
        assert result.price == 90.0
        assert result.category == "Bebida"
        mock_product_repository.get_by_id.assert_called_once_with(1)
        mock_product_repository.update.assert_called_once_with(product)

    def test_update_product_not_found(self, product_use_case, mock_product_repository):
        mock_product_repository.get_by_id.return_value = None
        updated_data = ProductSchema(name="Updated Product", price=90.0, category="Bebida")

        with pytest.raises(ValueError, match="Product not found"):
            product_use_case.update_product(product_id=999, product_data=updated_data)

    def test_delete_product_success(self, product_use_case, mock_product_repository):
        product = Products(id=1, name="Test Product", price=100.0, category="Lanche")
        mock_product_repository.get_by_id.return_value = product

        result = product_use_case.delete_product(product_id=1)

        assert result == {"message": "Product deleted"}
        mock_product_repository.delete.assert_called_once_with(product)

    def test_delete_product_not_found(self, product_use_case, mock_product_repository):
        mock_product_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="Product not found"):
            product_use_case.delete_product(product_id=999)
