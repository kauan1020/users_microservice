from tech.domain.entities.orders import Order, OrderStatus
from tech.interfaces.repositories.order_repository import OrderRepository
from tech.interfaces.repositories.product_repository import ProductRepository
from tech.interfaces.schemas.order_schema import OrderCreate, OrderPublic

class CreateOrderUseCase(object):
    """
    Handles the creation of a new order with the requested products.
    """

    def __init__(self, order_repository: OrderRepository, product_repository: ProductRepository):
        self.order_repository = order_repository
        self.product_repository = product_repository

    def execute(self, order_data: OrderCreate) -> OrderPublic:
        total_price = 0
        product_details = []

        for product_id in order_data.product_ids:
            product = self.product_repository.get_by_id(product_id)
            if not product:
                raise ValueError(f"Product with ID {product_id} not found")

            total_price += product.price
            product_details.append({
                "id": product.id,
                "name": product.name,
                "price": product.price,
            })

        order = Order(
            total_price=total_price,
            product_ids=','.join(map(str, order_data.product_ids)),
            status=OrderStatus.RECEIVED,
        )

        saved_order = self.order_repository.add(order)
        return OrderPublic(
            id=saved_order.id,
            total_price=saved_order.total_price,
            status=saved_order.status.value,
            products=product_details,
        )
