from typing import List
from tech.core.domain.models import Products
from tech.core.domain.schemas import ProductSchema
from tech.ports.repositories.product_repository import ProductRepository

class ProductUseCase(object):
    """Use case layer for handling Product-related business logic."""

    def __init__(self, product_repository: ProductRepository):
        """Initialize ProductUseCase with a repository.

        Args:
            product_repository (ProductRepository): The repository for Product-related database operations.
        """
        self.product_repository = product_repository

    def create_product(self, product_data: ProductSchema) -> Products:
        """Create a new product.

        Args:
            product_data (ProductSchema): Data schema for creating a new product.

        Returns:
            Products: The newly created product object.

        Raises:
            ValueError: If a product with the same name already exists.
        """
        existing_product = self.product_repository.get_by_name(product_data.name)
        if existing_product:
            raise ValueError('Product already exists')

        new_product = Products(
            name=product_data.name,
            price=product_data.price,
            category=product_data.category,
        )

        return self.product_repository.add(new_product)

    def get_product(self, product_id: int) -> Products:
        """Retrieve a product by its unique ID.

        Args:
            product_id (int): The ID of the product to retrieve.

        Returns:
            Products: The matching product object, if found.

        Raises:
            ValueError: If no product is found.
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError('Product not found')
        return product

    def list_products_by_category(self, category: str) -> List[Products]:
        """List products by their category.

        Args:
            category (str): The category to filter products by.

        Returns:
            List[Products]: A list of products matching the category.
        """
        return self.product_repository.list_by_category(category)

    def list_all_products(self) -> List[Products]:
        """List all products.

        Returns:
            List[Products]: A list of all available products.
        """
        return self.product_repository.list_all_products()

    def update_product(self, product_id: int, product_data: ProductSchema) -> Products:
        """Update a product's information.

        Args:
            product_id (int): The ID of the product to update.
            product_data (ProductSchema): The updated product data.

        Returns:
            Products: The updated product object.

        Raises:
            ValueError: If the product is not found.
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError('Product not found')

        product.name = product_data.name
        product.price = product_data.price
        product.category = product_data.category

        return self.product_repository.update(product)

    def delete_product(self, product_id: int) -> dict:
        """Delete a product by its unique ID.

        Args:
            product_id (int): The ID of the product to delete.

        Returns:
            dict: A success message.

        Raises:
            ValueError: If the product is not found.
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError('Product not found')
        self.product_repository.delete(product)
        return {"message": "Product deleted"}
