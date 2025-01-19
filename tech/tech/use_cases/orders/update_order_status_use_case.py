from tech.domain.entities.orders import OrderStatus
from tech.interfaces.schemas.order_schema import OrderStatusEnum
from tech.interfaces.repositories.order_repository import OrderRepository


class UpdateOrderStatusUseCase(object):
    """
    Handles updating the status of an existing order.

    Args:
        order_repository (OrderRepository): Repository to interact with order data.
    """

    def __init__(self, order_repository: OrderRepository):
        """
        Initialize the use case with the order repository.


        """
        self.order_repository = order_repository

    def execute(self, order_id: int, status: OrderStatusEnum) -> dict:
        """
        Update the status of an order by its ID.

        Args:
            order_id (int): The unique identifier of the order to update.
            status (OrderStatusEnum): The new status to assign to the order.

        Returns:
            dict: A success message confirming the status update.

        Raises:
            ValueError: If the order with the given ID does not exist.
        """
        new_status = OrderStatus(status.value)
        db_order = self.order_repository.get_by_id(order_id)
        if not db_order:
            raise ValueError("Order not found")

        db_order.status = new_status
        self.order_repository.update(db_order)
        return {"message": "Order status updated successfully"}
