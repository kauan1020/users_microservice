from tech.domain.entities.products import Products
from tech.interfaces.repositories.product_repository import ProductRepository

class GetProductUseCase(object):
    """
    Handles retrieving a product by its unique ID.
    """

    def __init__(self, product_repository: ProductRepository):
        """
        Initialize the use case with the product repository.

        Args:
            product_repository (ProductRepository): Repository to interact with product data.
        """
        self.product_repository = product_repository

    def execute(self, product_id: int) -> Products:
        """
        Retrieve a product by its ID.

        Args:
            product_id (int): The unique identifier of the product to retrieve.

        Returns:
            Products: The retrieved product entity.

        Raises:
            ValueError: If the product with the given ID does not exist.
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        return product
