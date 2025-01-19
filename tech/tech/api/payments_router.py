from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from tech.infra.databases.database import get_session
from tech.domain.entities.payments import PaymentStatus
from tech.infra.repositories.sql_alchemy_order_repository import SQLAlchemyOrderRepository
from tech.infra.repositories.sql_alchemy_payment_repository import SQLAlchemyPaymentRepository
from tech.interfaces.schemas.payment_schema import PaymentCreate, PaymentStatusResponse
from tech.use_cases.payments.create_payment_use_case import CreatePaymentUseCase
from tech.use_cases.payments.get_payment_status_use_case import GetPaymentStatusUseCase
from tech.use_cases.payments.webhook_payment_use_case import WebhookHandlerUseCase
from tech.interfaces.gateways.mock_payment_gateway import MockPaymentGateway

router = APIRouter()


def get_create_payment_use_case(
    session: Session = Depends(get_session)
) -> CreatePaymentUseCase:
    """
    Provides an instance of CreatePaymentUseCase with required dependencies.

    Args:
        session (Session): SQLAlchemy session dependency.

    Returns:
        CreatePaymentUseCase: The use case for creating payments.
    """
    return CreatePaymentUseCase(
        payment_gateway=MockPaymentGateway(),
        order_repository=SQLAlchemyOrderRepository(session),
        payment_repository=SQLAlchemyPaymentRepository(session),
    )


def get_get_payment_status_use_case(
    session: Session = Depends(get_session)
) -> GetPaymentStatusUseCase:
    """
    Provides an instance of GetPaymentStatusUseCase with required dependencies.

    Args:
        session (Session): SQLAlchemy session dependency.

    Returns:
        GetPaymentStatusUseCase: The use case for retrieving payment status.
    """
    return GetPaymentStatusUseCase(
        payment_repository=SQLAlchemyPaymentRepository(session)
    )


def get_webhook_handler_use_case(
    session: Session = Depends(get_session)
) -> WebhookHandlerUseCase:
    """
    Provides an instance of WebhookHandlerUseCase with required dependencies.

    Args:
        session (Session): SQLAlchemy session dependency.

    Returns:
        WebhookHandlerUseCase: The use case for handling webhook updates.
    """
    return WebhookHandlerUseCase(
        payment_repository=SQLAlchemyPaymentRepository(session)
    )


@router.post('/payments', response_model=PaymentStatusResponse, status_code=201)
def create_payment(
    payment_data: PaymentCreate,
    use_case: CreatePaymentUseCase = Depends(get_create_payment_use_case),
):
    """
    API endpoint to create a payment for an order.

    Args:
        payment_data (PaymentCreate): Data for creating the payment.
        use_case (CreatePaymentUseCase): Use case instance for creating payments.

    Returns:
        PaymentStatusResponse: Response with the payment details.
    """
    payment = use_case.execute(payment_data)
    return {
        "order_id": payment.order_id,
        "status": payment.status.value,
    }


@router.get('/payments/{order_id}', response_model=PaymentStatusResponse)
def get_payment_status(
    order_id: int,
    use_case: GetPaymentStatusUseCase = Depends(get_get_payment_status_use_case),
):
    """
    API endpoint to retrieve the payment status of an order.

    Args:
        order_id (int): The ID of the order.
        use_case (GetPaymentStatusUseCase): Use case instance for retrieving payment status.

    Returns:
        PaymentStatusResponse: The order ID and the current payment status.
    """
    try:
        status = use_case.execute(order_id)
        return {"order_id": order_id, "status": status.name}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post('/webhook', status_code=200)
def webhook_payment(
    order_id: int,
    status: str,
    use_case: WebhookHandlerUseCase = Depends(get_webhook_handler_use_case),
):
    """
    API endpoint to handle webhook payment status updates.

    Args:
        order_id (int): The ID of the order.
        status (str): The new payment status (approved/rejected).
        use_case (WebhookHandlerUseCase): Use case instance for handling webhook updates.

    Returns:
        dict: The updated payment status.

    Raises:
        HTTPException: If the payment is not found or if the status is invalid.
    """
    try:
        payment_status = PaymentStatus(status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payment status")

    try:
        updated_payment = use_case.execute(order_id, payment_status)
        return {"order_id": updated_payment.order_id, "status": updated_payment.status.value}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
