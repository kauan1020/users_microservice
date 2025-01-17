from tech.interfaces.gateways.payment_gateway import PaymentGateway
from tech.interfaces.repositories.order_repository import OrderRepository
from tech.interfaces.repositories.payment_repository import PaymentRepository
from tech.domain.entities.payments import Payment, PaymentStatus
from tech.interfaces.schemas.payment_schema import PaymentCreate


class CreatePaymentUseCase(object):
    """
    Use case for creating a payment.

    Handles the creation of payments by validating the order, calculating
    the amount, and storing the payment in the database.
    """

    def __init__(
        self,
        payment_gateway: PaymentGateway,
        order_repository: OrderRepository,
        payment_repository: PaymentRepository,
    ):
        """
        Initialize the CreatePaymentUseCase with dependencies.

        Args:
            payment_gateway (PaymentGateway): Gateway for interacting with payments.
            order_repository (OrderRepository): Repository for fetching order details.
            payment_repository (PaymentRepository): Repository for storing payment data.
        """
        self.payment_gateway = payment_gateway
        self.order_repository = order_repository
        self.payment_repository = payment_repository

    def execute(self, payment_data: PaymentCreate) -> Payment:
        """
        Create a new payment for an order.

        Args:
            payment_data (PaymentCreate): The payment data containing the order ID.

        Returns:
            Payment: The created payment with the initial status.
        """
        order = self.order_repository.get_by_id(payment_data.order_id)
        if not order:
            raise ValueError("Order not found")

        amount = order.total_price
        payment = Payment(
            order_id=payment_data.order_id,
            amount=amount,
            status=PaymentStatus.PENDING,
        )
        saved_payment = self.payment_repository.add(payment)
        return saved_payment

