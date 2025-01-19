from typing import Optional
from tech.domain.entities.payments import Payment, PaymentStatus


class PaymentRepository(object):
    """
    Interface for Payment Repository.

    Methods:
        add(payment: Payment) -> Payment: Save a new payment in the database.
        get_by_order_id(order_id: int) -> Optional[Payment]: Retrieve a payment by its order ID.
        update(payment: Payment) -> Payment: Update an existing payment.
    """

    def add(self, payment: Payment) -> Payment:
        """
        Save a new payment to the database.

        Args:
            payment (Payment): The payment to save.

        Returns:
            Payment: The saved payment.
        """
        raise NotImplementedError

    def get_by_order_id(self, order_id: int) -> Optional[Payment]:
        """
        Retrieve a payment by its order ID.

        Args:
            order_id (int): The order ID associated with the payment.

        Returns:
            Optional[Payment]: The payment if found, otherwise None.
        """
        raise NotImplementedError

    def update(self, payment: Payment) -> Payment:
        """
        Update an existing payment.

        Args:
            payment (Payment): The payment to update.

        Returns:
            Payment: The updated payment.
        """
        raise NotImplementedError
