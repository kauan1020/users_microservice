from sqlalchemy.orm import Session
from tech.domain.entities.orders import Order
from tech.interfaces.repositories.order_repository import OrderRepository
from tech.infra.repositories.sql_alchemy_order_repository import SQLAlchemyOrderRepository

class OrderGateway(OrderRepository):
    """
    Gateway that acts as an adapter between use cases and the database repository.

    This class ensures that use cases do not interact directly with the database repository,
    maintaining separation of concerns and improving maintainability.
    """

    def __init__(self, session: Session):
        """
        Initializes the OrderGateway with a database session.

        Args:
            session (Session): The SQLAlchemy session used for database transactions.
        """
        self.repository = SQLAlchemyOrderRepository(session)

    def add(self, order: Order) -> Order:
        """
        Adds a new order to the repository.

        Args:
            order (Order): The order entity to be added.

        Returns:
            Order: The added order with an assigned ID.
        """
        return self.repository.add(order)

    def get_by_id(self, order_id: int) -> Order:
        """
        Retrieves an order by its unique ID.

        Args:
            order_id (int): The unique identifier of the order.

        Returns:
            Order: The order entity if found, otherwise None.
        """
        return self.repository.get_by_id(order_id)

    def list_orders(self, limit: int, skip: int):
        """
        Retrieves a list of orders with pagination.

        Args:
            limit (int): The maximum number of orders to return.
            skip (int): The number of orders to skip.

        Returns:
            list: A list of order entities.
        """
        return self.repository.list_orders(limit, skip)

    def update(self, order: Order) -> Order:
        """
        Updates an existing order's information.

        Args:
            order (Order): The order entity with updated information.

        Returns:
            Order: The updated order entity.
        """
        return self.repository.update(order)

    def delete(self, order: Order):
        """
        Deletes an order from the repository.

        Args:
            order (Order): The order entity to be deleted.
        """
        return self.repository.delete(order)
