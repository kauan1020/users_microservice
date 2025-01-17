from tech.domain.entities.products import Products
from tech.interfaces.schemas.product_schema import ProductSchema
from tech.interfaces.repositories.product_repository import ProductRepository

class CreateProductUseCase(object):
    """
    Handles the creation of a new product.

    Ensures that no duplicate product exists and creates a new product entity
    with the provided details.
    """

    def __init__(self, product_repository: ProductRepository):
        """
        Initialize the use case with the product repository.

        Args:
            product_repository (ProductRepository): Repository to interact with product data.
        """
        self.product_repository = product_repository

    def execute(self, product_data: ProductSchema) -> Products:
        """
        Create a new product.

        Args:
            product_data (ProductSchema): Schema containing the details of the product to be created.

        Returns:
            Products: The newly created product entity.

        Raises:
            ValueError: If a product with the same name already exists.
        """
        existing_product = self.product_repository.get_by_name(product_data.name)
        if existing_product:
            raise ValueError("Product already exists")

        new_product = Products(
            name=product_data.name,
            price=product_data.price,
            category=product_data.category,
        )
        return self.product_repository.add(new_product)
