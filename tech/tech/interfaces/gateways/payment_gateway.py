from tech.domain.entities.payments import Payment, PaymentStatus


class PaymentGateway(object):
    """
    Interface for the Payment Gateway.

    This interface defines the methods for creating and retrieving payment status.
    Concrete implementations must adhere to this interface.
    """

    def create_payment(self, order_id: int, amount: float) -> Payment:
        """
        Creates a payment request for a specific order.

        Args:
            order_id (int): The ID of the associated order.
            amount (float): The amount to be charged for the order.

        Returns:
            Payment: A Payment entity with the created payment details.

        Raises:
            NotImplementedError: If not implemented by a concrete class.
        """
        raise NotImplementedError

    def get_payment_status(self, order_id: int) -> PaymentStatus:
        """
        Retrieves the payment status for a specific order.

        Args:
            order_id (int): The ID of the associated order.

        Returns:
            PaymentStatus: The current status of the payment.

        Raises:
            NotImplementedError: If not implemented by a concrete class.
        """
        raise NotImplementedError
