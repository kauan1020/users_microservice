class PaymentPresenter(object):
    """
    Formats the output for payment-related use cases.

    Methods:
        present_payment_status(order_id: int, status: str): Formats the payment status response.
    """

    @staticmethod
    def present_payment_status(order_id: int, status: str) -> dict:
        """
        Formats the payment status response.

        Args:
            order_id (int): The ID of the associated order.
            status (str): The current status of the payment.

        Returns:
            dict: A dictionary containing the order ID and payment status.
        """
        return {
            "order_id": order_id,
            "status": status
        }