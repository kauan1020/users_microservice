from tech.interfaces.gateways.payment_gateway import PaymentGateway
from tech.domain.entities.payments import Payment, PaymentStatus


class MockPaymentGateway(PaymentGateway):
    """
    Mock implementation of the PaymentGateway interface.

    This mock simulates a payment gateway, storing payments in memory
    and simulating status updates for testing purposes.
    """

    def __init__(self):
        """
        Initializes the mock payment gateway with an in-memory storage for payments.
        """
        self.payments = {}

    def create_payment(self, order_id: int, amount: float) -> Payment:
        """
        Simulates the creation of a payment request.

        Args:
            order_id (int): The ID of the order associated with the payment.
            amount (float): The amount to be charged for the payment.

        Returns:
            Payment: A Payment entity with a status of PENDING.
        """
        payment = Payment(order_id=order_id, amount=amount, status=PaymentStatus.PENDING)
        self.payments[order_id] = payment
        return payment

    def get_payment_status(self, order_id: int) -> PaymentStatus:
        """
        Simulates retrieving the payment status for a specific order.

        Args:
            order_id (int): The ID of the associated order.

        Returns:
            PaymentStatus: The updated status of the payment.

        Raises:
            ValueError: If the payment does not exist.
        """
        if order_id not in self.payments:
            raise ValueError("Payment not found")

        payment = self.payments[order_id]
        payment.status = PaymentStatus.APPROVED
        return payment.status

    def update_payment_status(self, order_id: int, status: PaymentStatus) -> Payment:
        """
        Simulates updating the payment status through a webhook.

        Args:
            order_id (int): The ID of the associated order.
            status (PaymentStatus): The new payment status.

        Returns:
            Payment: The updated Payment entity.

        Raises:
            ValueError: If the payment does not exist.
        """
        if order_id not in self.payments:
            raise ValueError("Payment not found")

        payment = self.payments[order_id]
        payment.status = status
        return payment
