from sqlalchemy.orm import Session
from tech.domain.entities.payments import Payment
from tech.interfaces.repositories.payment_repository import PaymentRepository
from tech.infra.repositories.sql_alchemy_payment_repository import SQLAlchemyPaymentRepository

class PaymentGateway(PaymentRepository):
    """
    Gateway that acts as an adapter between use cases and the database repository.
    """

    def __init__(self, session: Session):
        """
        Initializes the PaymentGateway with a database session.

        Args:
            session (Session): The SQLAlchemy session used for database transactions.
        """
        self.repository = SQLAlchemyPaymentRepository(session)

    def add(self, payment: Payment) -> Payment:
        """
        Adds a new payment to the repository.

        Args:
            payment (Payment): The payment entity to be added.

        Returns:
            Payment: The added payment with an assigned ID.
        """
        return self.repository.add(payment)

    def get_by_order_id(self, order_id: int) -> Payment:
        """
        Retrieves a payment by its order ID.

        Args:
            order_id (int): The unique identifier of the order.

        Returns:
            Payment: The payment entity if found, otherwise None.
        """
        return self.repository.get_by_order_id(order_id)

    def update(self, payment: Payment) -> Payment:
        """
        Updates an existing payment's information.

        Args:
            payment (Payment): The payment entity with updated information.

        Returns:
            Payment: The updated payment entity.
        """
        return self.repository.update(payment)
