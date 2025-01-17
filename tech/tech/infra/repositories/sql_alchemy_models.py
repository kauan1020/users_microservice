from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, create_engine
from sqlalchemy.orm import registry
from datetime import datetime
import enum

table_registry = registry()

class OrderStatus(enum.Enum):
    RECEIVED = 'RECEIVED'
    PREPARING = 'PREPARING'
    READY = 'READY'
    FINISHED = 'FINISHED'


@table_registry.mapped
class SQLAlchemyUser(object):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


@table_registry.mapped
class SQLAlchemyProduct(object):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


@table_registry.mapped
class SQLAlchemyOrder(object):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float, nullable=False)
    product_ids = Column(String,
                         nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.RECEIVED, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PaymentStatus(enum.Enum):
    """
    Enum representing the status of a payment.
    """
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'


@table_registry.mapped
class SQLAlchemyPayment(object):
    """
    SQLAlchemy mapping for the Payment entity.

    Attributes:
        order_id (int): The unique identifier of the associated order.
        amount (float): The total amount for the payment.
        status (PaymentStatus): The current status of the payment.
        created_at (datetime): The timestamp when the payment was created.
        updated_at (datetime): The timestamp when the payment was last updated.
    """
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)