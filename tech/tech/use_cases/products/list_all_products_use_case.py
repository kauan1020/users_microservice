from typing import List
from tech.domain.entities.products import Products
from tech.interfaces.repositories.product_repository import ProductRepository

class ListAllProductsUseCase(object):
    """
    Handles retrieving all products.
    """

    def __init__(self, product_repository: ProductRepository):
        """
        Initialize the use case with the product repository.

        Args:
            product_repository (ProductRepository): Repository to interact with product data.
        """
        self.product_repository = product_repository

    def execute(self) -> List[Products]:
        """
        Retrieve a list of all products.

        Returns:
            List[Products]: A list of all available products.
        """
        return self.product_repository.list_all_products()
