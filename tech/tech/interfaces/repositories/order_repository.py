from abc import ABC, abstractmethod
from typing import List, Optional
from tech.domain.entities.orders import Order

class OrderRepository(ABC):
    """Interface for the order repository, defining the operations
    that the infrastructure should implement."""

    @abstractmethod
    def add(self, order: Order) -> Order:
        """Adds a new order to the repository.

        Args:
            order (Order): The order entity to be added.

        Returns:
            Order: The added order with an assigned ID.
        """
        pass

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Retrieves an order by its ID.

        Args:
            order_id (int): The ID of the order.

        Returns:
            Optional[Order]: The order entity if found, otherwise None.
        """
        pass

    @abstractmethod
    def list_orders(self, limit: int, skip: int) -> List[Order]:
        """Retrieves a list of orders with pagination.

        Args:
            limit (int): The number of orders to retrieve.
            skip (int): The number of orders to skip before retrieving.

        Returns:
            List[Order]: A list of order entities.
        """
        pass

    @abstractmethod
    def update(self, order: Order) -> Order:
        """Updates an existing order's information.

        Args:
            order (Order): The order entity with updated information.

        Returns:
            Order: The updated order entity.
        """
        pass

    @abstractmethod
    def delete(self, order: Order) -> None:
        """Deletes an order from the repository.

        Args:
            order (Order): The order entity to be deleted.
        """
        pass
