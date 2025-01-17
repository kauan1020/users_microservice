from tech.domain.entities.payments import Payment, PaymentStatus
from tech.interfaces.repositories.payment_repository import PaymentRepository

class UpdatePaymentStatusUseCase(object):
    """
    Updates the status of a payment.

    Args:
        payment_repository (PaymentRepository): The repository interface for Payment-related operations.
    """

    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def execute(self, order_id: int, new_status: PaymentStatus) -> Payment:
        """
        Updates the status of a payment for the given order ID.

        Args:
            order_id (int): The unique identifier of the order.
            new_status (PaymentStatus): The new status to be set for the payment.

        Returns:
            Payment: The updated Payment object.

        Raises:
            ValueError: If the payment is not found or the status is invalid.
        """
        payment = self.payment_repository.get_by_order_id(order_id)
        if not payment:
            raise ValueError("Payment not found for this order.")

        payment.status = new_status
        return self.payment_repository.update(payment)
