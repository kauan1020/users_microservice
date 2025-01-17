from tech.interfaces.repositories.payment_repository import PaymentRepository
from tech.domain.entities.payments import PaymentStatus


class GetPaymentStatusUseCase(object):
    """
    Use case to retrieve the payment status for a specific order.
    """

    def __init__(self, payment_repository: PaymentRepository):
        """
        Initialize the use case with a payment repository.

        Args:
            payment_repository (PaymentRepository): The repository for accessing payment data.
        """
        self.payment_repository = payment_repository

    def execute(self, order_id: int) -> PaymentStatus:
        """
        Retrieve the payment status for a given order ID.

        Args:
            order_id (int): The ID of the order to fetch the payment status.

        Returns:
            PaymentStatus: The current payment status of the order.

        Raises:
            ValueError: If no payment is found for the given order ID.
        """
        payment = self.payment_repository.get_by_order_id(order_id)
        if not payment:
            raise ValueError("Payment not found for the given order ID.")

        return payment.status
