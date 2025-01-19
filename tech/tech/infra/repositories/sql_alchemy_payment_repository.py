from sqlalchemy.orm import Session
from tech.domain.entities.payments import Payment, PaymentStatus
from tech.interfaces.repositories.payment_repository import PaymentRepository
from tech.infra.repositories.sql_alchemy_models import SQLAlchemyPayment


class SQLAlchemyPaymentRepository(PaymentRepository):
    """
    SQLAlchemy implementation of the PaymentRepository interface.

    This repository provides methods to interact with the `payments` table in the database.
    """

    def __init__(self, session: Session):
        """
        Initialize the repository with a SQLAlchemy session.

        Args:
            session (Session): A SQLAlchemy session for database operations.
        """
        self.session = session

    def _to_domain_payment(self, db_payment: SQLAlchemyPayment) -> Payment:
        """
        Convert a SQLAlchemyPayment instance to a domain Payment instance.

        Args:
            db_payment (SQLAlchemyPayment): The SQLAlchemy model instance to convert.

        Returns:
            Payment: The corresponding domain model instance.
        """
        print(f"Valor do status retornado pelo banco: {db_payment.status}")
        return Payment(
            order_id=db_payment.order_id,
            amount=db_payment.amount,
            status=db_payment.status,
        )

    def _to_db_payment(self, payment: Payment) -> SQLAlchemyPayment:
        """
        Convert a domain Payment instance to a SQLAlchemyPayment instance.

        Args:
            payment (Payment): The domain model instance to convert.

        Returns:
            SQLAlchemyPayment: The corresponding SQLAlchemy model instance.
        """
        return SQLAlchemyPayment(
            order_id=payment.order_id,
            amount=payment.amount,
            status=payment.status,
        )

    def add(self, payment: Payment) -> Payment:
        """
        Save a new payment to the database.

        Args:
            payment (Payment): The payment to save.

        Returns:
            Payment: The saved payment with updated attributes.
        """
        db_payment = SQLAlchemyPayment(
            order_id=payment.order_id,
            amount=payment.amount,
            status=payment.status.name,
        )
        self.session.add(db_payment)
        self.session.commit()
        self.session.refresh(db_payment)
        return self._to_domain_payment(db_payment)

    def get_by_order_id(self, order_id: int) -> Payment:
        """
        Retrieve a payment by its order ID.

        Args:
            order_id (int): The order ID associated with the payment.

        Returns:
            Payment: The found payment.

        Raises:
            ValueError: If no payment is found for the given order ID.
        """
        db_payment = self.session.query(SQLAlchemyPayment).filter(SQLAlchemyPayment.order_id == order_id).first()
        if not db_payment:
            raise ValueError("Payment not found")
        return self._to_domain_payment(db_payment)

    def update(self, payment: Payment) -> Payment:
        """
        Update an existing payment.

        Args:
            payment (Payment): The payment to update.

        Returns:
            Payment: The updated payment.
        """
        db_payment = self.session.query(SQLAlchemyPayment).filter(
            SQLAlchemyPayment.order_id == payment.order_id).first()
        if not db_payment:
            raise ValueError("Payment not found")

        db_payment.amount = payment.amount
        db_payment.status = payment.status.name
        self.session.commit()
        self.session.refresh(db_payment)
        return self._to_domain_payment(db_payment)

    def create(self, payment: Payment) -> Payment:
        """
        Create a new payment record in the database.

        Args:
            payment (Payment): The Payment entity to be saved.

        Returns:
            Payment: The Payment entity with its database ID set.
        """
        db_payment = SQLAlchemyPayment(
            order_id=payment.order_id,
            amount=payment.amount,
            status=payment.status.value,
        )
        self.session.add(db_payment)
        self.session.commit()
        self.session.refresh(db_payment)

        payment.id = db_payment.id
        return payment