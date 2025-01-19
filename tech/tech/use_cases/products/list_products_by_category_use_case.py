from typing import List
from tech.domain.entities.products import Products
from tech.interfaces.repositories.product_repository import ProductRepository

class ListProductsByCategoryUseCase(object):
    """
    Handles retrieving products filtered by a specific category.
    """

    def __init__(self, product_repository: ProductRepository):
        """
        Initialize the use case with the product repository.

        Args:
            product_repository (ProductRepository): Repository to interact with product data.
        """
        self.product_repository = product_repository

    def execute(self, category: str) -> List[Products]:
        """
        Retrieve a list of products filtered by category.

        Args:
            category (str): The category to filter products by.

        Returns:
            List[Products]: A list of products in the specified category.
        """
        return self.product_repository.list_by_category(category)
