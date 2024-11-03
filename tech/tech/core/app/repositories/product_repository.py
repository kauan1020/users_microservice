from abc import ABC, abstractmethod
from typing import List, Optional
from tech.core.domain.models import Products

class ProductRepository(ABC):
    """Interface for the product repository, defining the operations
    that the infrastructure should implement."""

    @abstractmethod
    def add(self, product: Products) -> Products:
        """Adds a new product to the repository.

        Args:
            product (Products): The product entity to be added.

        Returns:
            Products: The added product with an assigned ID.
        """
        pass

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Products]:
        """Retrieves a product by its ID.

        Args:
            product_id (int): The ID of the product.

        Returns:
            Optional[Products]: The product entity if found, otherwise None.
        """
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Products]:
        """Fetches a product by its name.

        Args:
            name (str): The name of the product.

        Returns:
            Optional[Products]: The matching product entity if found, otherwise None.
        """
        pass

    @abstractmethod
    def list_by_category(self, category: str) -> List[Products]:
        """Retrieves a list of products by category.

        Args:
            category (str): The category of the products to retrieve.

        Returns:
            List[Products]: A list of matching product entities.
        """
        pass

    @abstractmethod
    def update(self, product: Products) -> Products:
        """Updates an existing product's information.

        Args:
            product (Products): The product entity with updated information.

        Returns:
            Products: The updated product entity.
        """
        pass

    @abstractmethod
    def delete(self, product: Products) -> None:
        """Deletes a product from the repository.

        Args:
            product (Products): The product entity to be deleted.
        """
        pass
