from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from tech.infra.databases.database import get_session
from tech.interfaces.gateways.order_gateway import OrderGateway
from tech.interfaces.schemas.order_schema import OrderCreate, OrderStatusEnum
from tech.use_cases.orders.create_order_use_case import CreateOrderUseCase
from tech.use_cases.orders.list_orders_use_case import ListOrdersUseCase
from tech.use_cases.orders.update_order_status_use_case import UpdateOrderStatusUseCase
from tech.use_cases.orders.delete_order_use_case import DeleteOrderUseCase
from tech.infra.repositories.sql_alchemy_product_repository import SQLAlchemyProductRepository
from tech.interfaces.controllers.order_controller import OrderController

router = APIRouter()

def get_order_controller(session: Session = Depends(get_session)) -> OrderController:
    """
    Dependency injection for the OrderController.

    This function initializes the controller by injecting the necessary use cases
    and the OrderGateway, ensuring proper separation of concerns.

    Args:
        session (Session): SQLAlchemy database session.

    Returns:
        OrderController: Instance of OrderController with required dependencies.
    """
    order_gateway = OrderGateway(session)
    product_repository = SQLAlchemyProductRepository(session)
    return OrderController(
        create_order_use_case=CreateOrderUseCase(order_gateway, product_repository),
        list_orders_use_case=ListOrdersUseCase(order_gateway, product_repository),
        update_order_status_use_case=UpdateOrderStatusUseCase(order_gateway, product_repository),
        delete_order_use_case=DeleteOrderUseCase(order_gateway),
    )


@router.post("/checkout", status_code=201)
def create_order(order: OrderCreate, controller: OrderController = Depends(get_order_controller)) -> dict:
    """
    Creates a new order.

    Args:
        order (OrderCreate): The order details to be created.
        controller (OrderController): The OrderController instance.

    Returns:
        dict: The formatted response containing order details.
    """
    return controller.create_order(order)

@router.get("/")
def list_orders(limit: int = 10, skip: int = 0, controller: OrderController = Depends(get_order_controller)) -> list:
    """
    Retrieves a paginated list of orders.

    Args:
        limit (int): The maximum number of orders to return.
        skip (int): The number of orders to skip.
        controller (OrderController): The OrderController instance.

    Returns:
        list: A list of formatted order details.
    """
    return controller.list_orders(limit, skip)

@router.put("/{order_id}")
def update_order_status(order_id: int, status: OrderStatusEnum, controller: OrderController = Depends(get_order_controller)) -> dict:
    """
    Updates the status of an order.

    Args:
        order_id (int): The ID of the order to update.
        status (OrderStatusEnum): The new status for the order.
        controller (OrderController): The OrderController instance.

    Returns:
        dict: A success message confirming the update.
    """
    return controller.update_order_status(order_id, status)

@router.delete("/{order_id}")
def delete_order(order_id: int, controller: OrderController = Depends(get_order_controller)) -> dict:
    """
    Deletes an order by its ID.

    Args:
        order_id (int): The ID of the order to delete.
        controller (OrderController): The OrderController instance.

    Returns:
        dict: A success message confirming deletion.
    """
    return controller.delete_order(order_id)
