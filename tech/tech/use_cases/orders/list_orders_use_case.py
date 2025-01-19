from tech.interfaces.schemas.order_schema import OrderStatusEnum
from tech.interfaces.repositories.order_repository import OrderRepository
from tech.interfaces.repositories.product_repository import ProductRepository


class ListOrdersUseCase(object):
    """
    Handles listing of orders with details including associated products and their prices.

    Orders are returned in a paginated format, with product details and metadata included.

    Args:
        order_repository (OrderRepository): Repository to fetch order data.
        product_repository (ProductRepository): Repository to fetch product details for orders.

    """

    def __init__(self, order_repository: OrderRepository, product_repository: ProductRepository):

        self.order_repository = order_repository
        self.product_repository = product_repository

    def execute(self, limit: int, skip: int) -> list:
        """
        Retrieve a paginated list of orders with their details.

        Args:
            limit (int): Maximum number of orders to retrieve.
            skip (int): Number of orders to skip before starting retrieval.

        Returns:
            list: List of orders, each containing product details, status, and metadata.

        Raises:
            None
        """
        orders = self.order_repository.list_orders(limit, skip)
        order_list = []

        for order in orders:
            product_ids = list(map(int, order.product_ids.split(',')))
            product_details = [
                self.product_repository.get_by_id(product_id) for product_id in product_ids
            ]

            order_list.append({
                "id": order.id,
                "total_price": order.total_price,
                "status": OrderStatusEnum(order.status.value),
                "products": [
                    {
                        "id": product.id,
                        "name": product.name,
                        "price": product.price,
                    } for product in product_details if product
                ],
                "created_at": order.created_at,
                "updated_at": order.updated_at,
            })

        return order_list
