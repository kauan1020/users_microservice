from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from tech.infra.databases.database import get_session
from tech.interfaces.schemas.order_schema import OrderCreate, OrderList, OrderPublic, OrderStatusEnum
from tech.interfaces.schemas.message_schema import Message
from tech.use_cases.orders.create_order_use_case import CreateOrderUseCase
from tech.use_cases.orders.list_orders_use_case import ListOrdersUseCase
from tech.use_cases.orders.update_order_status_use_case import UpdateOrderStatusUseCase
from tech.use_cases.orders.delete_order_use_case import DeleteOrderUseCase
from tech.infra.repositories.sql_alchemy_order_repository import SQLAlchemyOrderRepository
from tech.infra.repositories.sql_alchemy_product_repository import SQLAlchemyProductRepository

router = APIRouter()


def get_create_order_use_case(session: Session = Depends(get_session)):
    """
    Dependency injection for CreateOrderUseCase with repositories.

    Args:
        session (Session): SQLAlchemy session for database operations.

    Returns:
        CreateOrderUseCase: Use case instance configured with required repositories.
    """
    return CreateOrderUseCase(
        SQLAlchemyOrderRepository(session),
        SQLAlchemyProductRepository(session),
    )


def get_list_orders_use_case(session: Session = Depends(get_session)):
    """
    Dependency injection for ListOrdersUseCase with repositories.

    Args:
        session (Session): SQLAlchemy session for database operations.

    Returns:
        ListOrdersUseCase: Use case instance configured with required repositories.
    """
    return ListOrdersUseCase(
        SQLAlchemyOrderRepository(session),
        SQLAlchemyProductRepository(session),
    )


def get_update_order_status_use_case(session: Session = Depends(get_session)):
    """
    Dependency injection for UpdateOrderStatusUseCase.

    Args:
        session (Session): SQLAlchemy session for database operations.

    Returns:
        UpdateOrderStatusUseCase: Use case instance configured with the order repository.
    """
    return UpdateOrderStatusUseCase(SQLAlchemyOrderRepository(session))


def get_delete_order_use_case(session: Session = Depends(get_session)):
    """
    Dependency injection for DeleteOrderUseCase.

    Args:
        session (Session): SQLAlchemy session for database operations.

    Returns:
        DeleteOrderUseCase: Use case instance configured with the order repository.
    """
    return DeleteOrderUseCase(SQLAlchemyOrderRepository(session))


@router.post("/checkout", response_model=OrderPublic, status_code=201)
def create_order(order: OrderCreate, use_case: CreateOrderUseCase = Depends(get_create_order_use_case)):
    """
    API endpoint for creating a new order (checkout).

    Args:
        order (OrderCreate): The list of product IDs to include in the order.
        use_case (CreateOrderUseCase): The use case for handling order creation.

    Returns:
        OrderPublic: The created order's public details.

    Raises:
        HTTPException: If any of the products are not found.
    """
    try:
        return use_case.execute(order)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=OrderList)
def list_orders(limit: int = 10, skip: int = 0, use_case: ListOrdersUseCase = Depends(get_list_orders_use_case)):
    """
    List all orders with pagination.

    Args:
        limit (int): Maximum number of orders to retrieve. Defaults to 10.
        skip (int): Number of orders to skip before starting retrieval. Defaults to 0.
        use_case (ListOrdersUseCase): Use case to handle the business logic for listing orders.

    Returns:
        OrderList: Paginated list of orders.
    """
    return {"orders": use_case.execute(limit, skip)}


@router.put("/{order_id}", status_code=200)
def update_order_status(order_id: int, status: OrderStatusEnum, use_case: UpdateOrderStatusUseCase = Depends(get_update_order_status_use_case)):
    """
    Update the status of an order.

    Args:
        order_id (int): ID of the order to update.
        status (OrderStatusEnum): New status to assign to the order.
        use_case (UpdateOrderStatusUseCase): Use case to handle the business logic for updating order status.

    Returns:
        dict: A success message.

    Raises:
        HTTPException: If the order is not found or the update fails.
    """
    try:
        return use_case.execute(order_id, status)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{order_id}", response_model=Message)
def delete_order(order_id: int, use_case: DeleteOrderUseCase = Depends(get_delete_order_use_case)):
    """
    Delete an order by ID.

    Args:
        order_id (int): ID of the order to delete.
        use_case (DeleteOrderUseCase): Use case to handle the business logic for deleting orders.

    Returns:
        Message: A success message confirming deletion.

    Raises:
        HTTPException: If the order is not found.
    """
    try:
        return use_case.execute(order_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
