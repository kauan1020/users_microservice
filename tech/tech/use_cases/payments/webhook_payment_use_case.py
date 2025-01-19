from tech.domain.entities.payments import PaymentStatus
from tech.interfaces.repositories.payment_repository import PaymentRepository

class WebhookHandlerUseCase(object):
    """
    Handles payment status updates received via a webhook.

    Args:
        payment_repository (PaymentRepository): The repository interface for Payment-related operations.
    """

    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository

    def execute(self, order_id: int, payment_status: str) -> dict:
        """
        Processes a webhook notification to update the payment status.

        Args:
            order_id (int): The unique identifier of the order.
            payment_status (str): The new payment status received from the webhook.
                                  Can be a string (e.g., 'APPROVED') or an instance of PaymentStatus.

        Returns:
            dict: A success message indicating the updated status.

        Raises:
            ValueError: If the payment is not found or the status is invalid.
        """
        if isinstance(payment_status, PaymentStatus):
            payment_status_enum = payment_status
        else:
            if payment_status not in PaymentStatus.__members__:
                raise ValueError(f"Invalid payment status: {payment_status}")
            payment_status_enum = PaymentStatus[payment_status]

        payment = self.payment_repository.get_by_order_id(order_id)
        if not payment:
            raise ValueError("Payment not found for this order.")

        payment.status = payment_status_enum
        self.payment_repository.update(payment)
        return payment
