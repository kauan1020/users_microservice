from tech.domain.entities.products import Products
from tech.interfaces.schemas.product_schema import ProductSchema
from tech.interfaces.repositories.product_repository import ProductRepository

class UpdateProductUseCase(object):
    """
    Handles updating the details of an existing product.
    """

    def __init__(self, product_repository: ProductRepository):
        """
        Initialize the use case with the product repository.

        Args:
            product_repository (ProductRepository): Repository to interact with product data.
        """
        self.product_repository = product_repository

    def execute(self, product_id: int, product_data: ProductSchema) -> Products:
        """
        Update a product's details.

        Args:
            product_id (int): The unique identifier of the product to update.
            product_data (ProductSchema): Schema containing updated product details.

        Returns:
            Products: The updated product entity.

        Raises:
            ValueError: If the product with the given ID does not exist.
        """
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        product.name = product_data.name
        product.price = product_data.price
        product.category = product_data.category
        return self.product_repository.update(product)
