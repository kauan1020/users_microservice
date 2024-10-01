from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from tech.adapters.driven.infra.database import get_session
from tech.core.domain.models import Products
from tech.core.domain.schemas import ProductPublic, ProductSchema, Message

router = APIRouter()


def get_product_or_404(product_id: int, session: Session):
    product = session.scalar(select(Products).where(Products.id == product_id))
    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )
    return product


@router.post('/', status_code=HTTPStatus.CREATED, response_model=ProductPublic)
def create_product(
    product: ProductSchema, session: Session = Depends(get_session)
):
    db_product = Products(
        name=product.name, price=product.price, category=product.category
    )

    session.add(db_product)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Name already exists'
        )

    session.refresh(db_product)
    return db_product


@router.get('/{category}', response_model=list[ProductPublic])
def list_product_by_category(
    category: str, session: Session = Depends(get_session)
):
    db_products = session.scalars(
        select(Products).where(Products.category == category)
    ).all()

    if not db_products:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'No products found in category "{category}"',
        )

    return db_products


@router.put('/{product_id}', response_model=ProductPublic)
def update_product(
    product_id: int,
    product: ProductSchema,
    session: Session = Depends(get_session),
):
    db_product = get_product_or_404(product_id, session)

    db_product.name = product.name
    db_product.price = product.price
    db_product.category = product.category

    session.commit()
    session.refresh(db_product)

    return db_product


@router.delete('/{product_id}', response_model=Message)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    db_product = get_product_or_404(product_id, session)

    session.delete(db_product)
    session.commit()

    return {'message': 'Product deleted successfully'}
