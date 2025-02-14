class PaymentPresenter:
    """
    Handles the formatting of payment-related responses.
    """

    @staticmethod
    def present_payment_status(order_id: int, status: str) -> dict:
        """
        Formats a payment status response.

        Args:
            order_id (int): The order ID associated with the payment.
            status (str): The current payment status.

        Returns:
            dict: A dictionary containing the formatted payment details.
        """
        return {
            "order_id": order_id,
            "status": status
        }
