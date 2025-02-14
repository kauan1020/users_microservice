from fastapi import HTTPException
from tech.use_cases.orders.create_order_use_case import CreateOrderUseCase
from tech.use_cases.orders.list_orders_use_case import ListOrdersUseCase
from tech.use_cases.orders.update_order_status_use_case import UpdateOrderStatusUseCase
from tech.use_cases.orders.delete_order_use_case import DeleteOrderUseCase
from tech.interfaces.presenters.order_presenter import OrderPresenter
from tech.interfaces.schemas.order_schema import OrderCreate
from tech.domain.entities.orders import OrderStatus

class OrderController:
    """
    Controller responsible for managing order-related operations.
    """

    def __init__(
        self,
        create_order_use_case: CreateOrderUseCase,
        list_orders_use_case: ListOrdersUseCase,
        update_order_status_use_case: UpdateOrderStatusUseCase,
        delete_order_use_case: DeleteOrderUseCase
    ):
        """
        Initializes the OrderController with the required use cases.

        Args:
            create_order_use_case (CreateOrderUseCase): Use case for creating an order.
            list_orders_use_case (ListOrdersUseCase): Use case for listing orders.
            update_order_status_use_case (UpdateOrderStatusUseCase): Use case for updating order status.
            delete_order_use_case (DeleteOrderUseCase): Use case for deleting an order.
        """
        self.create_order_use_case = create_order_use_case
        self.list_orders_use_case = list_orders_use_case
        self.update_order_status_use_case = update_order_status_use_case
        self.delete_order_use_case = delete_order_use_case

    def create_order(self, order_data: OrderCreate) -> dict:
        """
        Creates a new order and returns a formatted response.

        Args:
            order_data (OrderCreate): The data required to create a new order.

        Returns:
            dict: The formatted response containing order details.

        Raises:
            HTTPException: If any of the products are not found.
        """
        try:
            order = self.create_order_use_case.execute(order_data)
            return OrderPresenter.present_order(order)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    def list_orders(self, limit: int, skip: int) -> list:
        """
        Retrieves a paginated list of orders.

        Args:
            limit (int): The maximum number of orders to return.
            skip (int): The number of orders to skip.

        Returns:
            list: A list of formatted order details.
        """
        orders = self.list_orders_use_case.execute(limit, skip)
        return OrderPresenter.present_order_list(orders)

    def update_order_status(self, order_id: int, status: OrderStatus) -> dict:
        """
        Updates the status of an order.

        Args:
            order_id (int): The ID of the order to update.
            status (OrderStatus): The new status for the order.

        Returns:
            dict: A success message.

        Raises:
            HTTPException: If the order is not found or the update fails.
        """
        try:
            updated_order = self.update_order_status_use_case.execute(order_id, status)
            return OrderPresenter.present_order(updated_order)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    def delete_order(self, order_id: int) -> dict:
        """
        Deletes an order by its unique ID.

        Args:
            order_id (int): The ID of the order to delete.

        Returns:
            dict: A success message confirming deletion.

        Raises:
            HTTPException: If the order is not found.
        """
        try:
            return self.delete_order_use_case.execute(order_id)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
