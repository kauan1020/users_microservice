from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from tech.infra.databases.database import get_session
from tech.interfaces.gateways.order_gateway import OrderGateway
from tech.interfaces.gateways.payment_gateway import PaymentGateway
from tech.interfaces.schemas.payment_schema import PaymentCreate
from tech.use_cases.payments.create_payment_use_case import CreatePaymentUseCase
from tech.use_cases.payments.get_payment_status_use_case import GetPaymentStatusUseCase
from tech.use_cases.payments.webhook_payment_use_case import WebhookHandlerUseCase
from tech.interfaces.controllers.payment_controller import PaymentController

router = APIRouter()

def get_payment_controller(session: Session = Depends(get_session)) -> PaymentController:
    """
    Dependency injection for the PaymentController.

    Args:
        session (Session): SQLAlchemy database session.

    Returns:
        PaymentController: Instance of PaymentController with required dependencies.
    """
    order_gateway = OrderGateway(session)
    payment_gateway = PaymentGateway(session)
    return PaymentController(
        create_payment_use_case=CreatePaymentUseCase(payment_gateway, order_gateway, payment_gateway),
        get_payment_status_use_case=GetPaymentStatusUseCase(payment_gateway),
        webhook_handler_use_case=WebhookHandlerUseCase(payment_gateway),
    )

@router.post("/payments", status_code=201)
def create_payment(payment_data: PaymentCreate, controller: PaymentController = Depends(get_payment_controller)) -> dict:
    """
    Creates a new payment.

    Args:
        payment_data (PaymentCreate): The payment details to be created.
        controller (PaymentController): The PaymentController instance.

    Returns:
        dict: The formatted response containing payment details.
    """
    return controller.create_payment(payment_data)

@router.get("/payments/{order_id}")
def get_payment_status(order_id: int, controller: PaymentController = Depends(get_payment_controller)) -> dict:
    """
    Retrieves the payment status of an order.

    Args:
        order_id (int): The order ID.
        controller (PaymentController): The PaymentController instance.

    Returns:
        dict: The formatted response containing payment status.
    """
    return controller.get_payment_status(order_id)

@router.post("/webhook")
def webhook_payment(order_id: int, status: str, controller: PaymentController = Depends(get_payment_controller)) -> dict:
    """
    Handles payment status updates via webhook.

    Args:
        order_id (int): The order ID.
        status (str): The new payment status.
        controller (PaymentController): The PaymentController instance.

    Returns:
        dict: The updated payment status.
    """
    return controller.webhook_payment(order_id, status)
