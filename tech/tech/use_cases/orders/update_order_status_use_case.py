from tech.domain.entities.orders import OrderStatus
from tech.interfaces.repositories.product_repository import ProductRepository
from tech.interfaces.schemas.order_schema import OrderStatusEnum, OrderPublic
from tech.interfaces.repositories.order_repository import OrderRepository


class UpdateOrderStatusUseCase(object):
    """
    Handles updating the status of an existing order.

    Args:
        order_repository (OrderRepository): Repository to interact with order data.
        product_repository (ProductRepository): Repository to interact with product data.

    """

    def __init__(self, order_repository: OrderRepository, product_repository: ProductRepository):
        """
        Initialize the use case with the order repository.


        """
        self.order_repository = order_repository
        self.product_repository = product_repository

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
        updated_order = self.order_repository.update(db_order)

        product_ids = list(map(int, updated_order.product_ids.split(',')))
        product_details = [
            self.product_repository.get_by_id(product_id) for product_id in product_ids
        ]

        return OrderPublic(
            id=updated_order.id,
            total_price=updated_order.total_price,
            status=updated_order.status.value,
            products=[{
                "id": product.id,
                "name": product.name,
                "price": product.price,
            } for product in product_details if product],
            created_at=updated_order.created_at,
            updated_at=updated_order.updated_at,
        )
