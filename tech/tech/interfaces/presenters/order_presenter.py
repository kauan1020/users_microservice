class OrderPresenter:
    """
    Handles the formatting of order-related responses.
    """

    @staticmethod
    def present_order(order: object) -> dict:
        """
        Formats a single order response.

        Args:
            order (object): The order entity to format.

        Returns:
            dict: A dictionary containing the formatted order details.
        """
        return {
            "id": order.id,
            "total_price": order.total_price,
            "product_ids": order.products,
            "status": order.status
        }

    @staticmethod
    def present_order_list(orders: list) -> list:
        """
        Formats a list of orders.

        Args:
            orders (list): A list of order entities.

        Returns:
            list: A list of dictionaries containing formatted order details.
        """
        return [OrderPresenter.present_order(order) for order in orders]
