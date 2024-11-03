from tech.core.domain.models import Order, OrderStatus
from tech.core.domain.schemas import OrderCreate, OrderStatusEnum
from tech.core.app.repositories.order_repository import OrderRepository
from tech.core.app.repositories.product_repository import ProductRepository

class OrderUseCase(object):
    """Use case layer for handling Order-related business logic."""

    def __init__(self, order_repository: OrderRepository, product_repository: ProductRepository):
        """Initialize OrderUseCase with repositories.

        Args:
            order_repository (OrderRepository): The repository for Order-related database operations.
            product_repository (ProductRepository): The repository for Product-related database operations.
        """
        self.order_repository = order_repository
        self.product_repository = product_repository

    def create_order(self, order_data: OrderCreate) -> dict:
        """Create a new order with the given products.

        Args:
            order_data (OrderCreate): The data for creating a new order.

        Returns:
            dict: The created order information, including products and total price.

        Raises:
            ValueError: If any of the products in the order cannot be found.
        """
        total_price = 0
        product_details = []

        for product_id in order_data.product_ids:
            product = self.product_repository.get_by_id(product_id)
            if not product:
                raise ValueError(f'Product with ID {product_id} not found')

            total_price += product.price
            product_details.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
            })

        db_order = Order(
            total_price=total_price,
            product_ids=','.join(map(str, order_data.product_ids)),
            status=OrderStatus.RECEIVED,
        )

        new_order = self.order_repository.add(db_order)

        return {
            'id': new_order.id,
            'total_price': new_order.total_price,
            'status': OrderStatusEnum(new_order.status.value),
            'products': product_details,
        }

    def list_orders(self, limit: int, skip: int):
        """List all orders with pagination.

        Args:
            limit (int): The number of orders to retrieve.
            skip (int): The number of orders to skip.

        Returns:
            List[dict]: A list of orders with their details.
        """
        orders = self.order_repository.list_orders(limit, skip)
        order_list = []

        for order in orders:
            product_ids = list(map(int, order.product_ids.split(',')))
            product_details = [
                self.product_repository.get_by_id(product_id) for product_id in product_ids
            ]

            order_list.append({
                'id': order.id,
                'total_price': order.total_price,
                'status': OrderStatusEnum(order.status.value),
                'products': [
                    {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                    } for product in product_details if product
                ],
                'created_at': order.created_at,
                'updated_at': order.updated_at,
            })

        return order_list

    def update_order_status(self, order_id: int, status: OrderStatusEnum) -> dict:
        """Update the status of an order.

        Args:
            order_id (int): The ID of the order to update.
            status (OrderStatusEnum): The new status for the order.

        Returns:
            dict: A success message.

        Raises:
            ValueError: If the order is not found.
        """
        new_status = OrderStatus(status.value)
        db_order = self.order_repository.get_by_id(order_id)
        if not db_order:
            raise ValueError('Order not found')

        db_order.status = new_status
        self.order_repository.update(db_order)
        return {"message": "Order status updated successfully"}

    def delete_order(self, order_id: int):
        """Delete an order by its unique ID.

        Args:
            order_id (int): The ID of the order to delete.

        Returns:
            dict: A success message.

        Raises:
            ValueError: If the order is not found.
        """
        db_order = self.order_repository.get_by_id(order_id)
        if not db_order:
            raise ValueError('Order not found')

        self.order_repository.delete(db_order)
        return {'message': 'Order deleted successfully'}
