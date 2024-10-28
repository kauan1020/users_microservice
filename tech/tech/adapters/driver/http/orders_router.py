from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tech.adapters.driven.infra.database import get_session
from tech.core.domain.schemas import OrderCreate, OrderList, OrderPublic, Message, OrderStatusEnum
from tech.core.use_cases.orders_use_cases import OrderUseCase
from tech.adapters.driven.infra.repositories.sql_alchemy_order_repository import SQLAlchemyOrderRepository
from tech.adapters.driven.infra.repositories.sql_alchemy_product_repository import SQLAlchemyProductRepository

router = APIRouter()

def get_order_use_case(session: Session = Depends(get_session)) -> OrderUseCase:
    """Dependency injection for OrderUseCase using the SQLAlchemy repositories.

    Args:
        session (Session): SQLAlchemy session for database operations.

    Returns:
        OrderUseCase: The use case with a repository configured.
    """
    order_repository = SQLAlchemyOrderRepository(session)
    product_repository = SQLAlchemyProductRepository(session)
    return OrderUseCase(order_repository, product_repository)

@router.post('/', response_model=OrderPublic, status_code=201)
def create_order(order: OrderCreate, use_case: OrderUseCase = Depends(get_order_use_case)):
    """Create a new order with the specified products.

    Args:
        order (OrderCreate): The data for creating a new order.
        use_case (OrderUseCase): The use case for order-related operations.

    Returns:
        OrderPublic: The created order's details including total price and products.

    Raises:
        HTTPException: If any of the products are not found.
    """
    try:
        created_order = use_case.create_order(order)
        return created_order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get('/', response_model=OrderList)
def list_orders(
    limit: int = 10,
    skip: int = 0,
    use_case: OrderUseCase = Depends(get_order_use_case)
):
    """Retrieve a paginated list of orders.

    Args:
        limit (int, optional): The number of orders to retrieve. Defaults to 10.
        skip (int, optional): The number of orders to skip. Defaults to 0.
        use_case (OrderUseCase): The use case for order-related operations.

    Returns:
        OrderList: A list of orders with their details.
    """
    orders = use_case.list_orders(limit, skip)
    return {'orders': orders}

@router.put('/{order_id}', status_code=200)
def update_order_status(
    order_id: int,
    status: OrderStatusEnum,
    use_case: OrderUseCase = Depends(get_order_use_case)
):
    """Update the status of an order.

    Args:
        order_id (int): The ID of the order to update.
        status (OrderStatusEnum): The new status for the order.
        use_case (OrderUseCase): The use case for order-related operations.

    Returns:
        dict: A success message.

    Raises:
        HTTPException: If the order is not found.
    """
    try:
        return use_case.update_order_status(order_id, status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete('/{order_id}', response_model=Message)
def delete_order(
    order_id: int,
    use_case: OrderUseCase = Depends(get_order_use_case)
):
    """Delete an order by ID.

    Args:
        order_id (int): The ID of the order to delete.
        use_case (OrderUseCase): The use case for order-related operations.

    Returns:
        Message: A success message.

    Raises:
        HTTPException: If the order is not found.
    """
    try:
        return use_case.delete_order(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
