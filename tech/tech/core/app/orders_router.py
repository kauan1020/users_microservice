from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from tech.adapters.driven.infra.database import get_session
from tech.core.domain.models import Order, Products, OrderStatus
from tech.core.domain.schemas import OrderCreate, OrderList, Message

router = APIRouter()


@router.post('/', status_code=201)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    total_price = 0
    product_details = []

    for product_id in order.product_ids:
        product = session.scalar(
            select(Products).where(Products.id == product_id)
        )
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f'Product with ID {product_id} not found',
            )

        total_price += product.price
        product_details.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
        })

    db_order = Order(
        total_price=total_price,
        product_ids=','.join(map(str, order.product_ids)),
        status=OrderStatus.RECEIVED,
    )

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return {
        'id': db_order.id,
        'total_price': db_order.total_price,
        'status': db_order.status.value,
        'products': product_details,
    }


@router.get('/', response_model=OrderList)
def list_orders(
    limit: int = 10, skip: int = 0, session: Session = Depends(get_session)
):
    orders = session.scalars(select(Order).limit(limit).offset(skip)).all()
    order_list = []

    for order in orders:
        product_ids = list(map(int, order.product_ids.split(',')))
        product_details = []

        for product_id in product_ids:
            product = session.scalar(
                select(Products).where(Products.id == product_id)
            )
            if product:
                product_details.append({
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                })

        order_list.append({
            'id': order.id,
            'total_price': order.total_price,
            'status': order.status.value,
            'products': product_details,
            'created_at': order.created_at,
            'updated_at': order.updated_at,
        })

    return {'orders': order_list}


@router.put('/{order_id}', status_code=200)
def update_order_status(
    order_id: int, status: OrderStatus, session: Session = Depends(get_session)
):
    db_order = session.scalar(select(Order).where(Order.id == order_id))
    if not db_order:
        raise HTTPException(status_code=404, detail='Order not found')

    db_order.status = status
    session.commit()
    session.refresh(db_order)

    return {'message': 'Order status updated successfully'}


@router.delete('/{order_id}', response_model=Message)
def delete_order(order_id: int, session: Session = Depends(get_session)):
    db_order = session.scalar(select(Order).where(Order.id == order_id))
    if not db_order:
        raise HTTPException(status_code=404, detail='Order not found')

    session.delete(db_order)
    session.commit()

    return {'message': 'Order deleted successfully'}
