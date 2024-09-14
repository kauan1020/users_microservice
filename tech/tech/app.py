from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from tech.database import get_session
from tech.models import Products, User, Order, OrderStatus
from tech.security import get_cpf_hash, get_password_hash
from tech.schemas import (
    Message,
    UserList,
    UserPublic,
    UserSchema,
    ProductPublic,
    ProductSchema,
    OrderCreate,
    OrderList,
)


app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Tech Challenge FIAP - Kauan Silva!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    if len(user.cpf) != 11 or not user.cpf.isdigit():
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='CPF must contain exactly 11 digits and be numeric.',
        )

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username)
            | (User.email == user.email)
            | (User.cpf == user.cpf)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )
        elif db_user.cpf == user.cpf:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='CPF already exists',
            )

    db_user = User(
        username=user.username,
        password=get_password_hash(user.password),
        cpf=user.cpf,
        email=user.email,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 10, skip: int = 0, session: Session = Depends(get_session)
):
    user = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': user}


@app.get('/users/{cpf}', response_model=UserPublic)
def list_user_with_cpf(cpf: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.cpf == cpf))

    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')

    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    db_user.username = user.username
    db_user.password = get_password_hash(user.password)
    db_user.email = user.email
    db_user.cpf = get_cpf_hash(user.cpf)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where((User.id == user_id)))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}


def get_product_or_404(product_id: int, session: Session):
    product = session.scalar(select(Products).where(Products.id == product_id))
    if not product:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Product not found'
        )
    return product


@app.post(
    '/products/', status_code=HTTPStatus.CREATED, response_model=ProductPublic
)
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


@app.get('/products/{category}', response_model=list[ProductPublic])
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


@app.put('/products/{product_id}', response_model=ProductPublic)
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


@app.delete('/products/{product_id}', response_model=Message)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    db_product = get_product_or_404(product_id, session)

    session.delete(db_product)
    session.commit()

    return {'message': 'Product deleted successfully'}


@app.post('/checkout/', status_code=HTTPStatus.CREATED)
def fake_checkout(order: OrderCreate, session: Session = Depends(get_session)):
    total_price = 0

    product_details = []

    for product_id in order.product_ids:
        product = session.scalar(
            select(Products).where(Products.id == product_id)
        )
        if not product:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
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


@app.get('/orders/', response_model=OrderList)
def list_orders(
    limit: int = 10, skip: int = 0, session: Session = Depends(get_session)
):
    orders = session.scalars(select(Order).limit(limit).offset(skip)).all()
    order_list = []

    for order in orders:
        product_ids = list(map(int, order.product_ids.split(',')))
        product_details = []

        for product_id in product_ids:
            product = session.scalar(select(Products).where(Products.id == product_id))
            if product:
                product_details.append({
                    "id": product.id,
                    "name": product.name,
                    "price": product.price
                })

        order_list.append({
            'id': order.id,
            'total_price': order.total_price,
            'status': order.status.value,
            'products': product_details,
            'created_at': order.created_at,
            'updated_at': order.updated_at
        })

    return {'orders': order_list}

