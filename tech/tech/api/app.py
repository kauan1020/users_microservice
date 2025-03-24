from http import HTTPStatus

from fastapi import FastAPI

from tech.api import orders_router, users_router, products_router, payments_router, auth_router
from tech.interfaces.schemas.message_schema import (
    Message,
)


app = FastAPI()
app.include_router(users_router.router, prefix='/users', tags=['users'])
app.include_router(
    products_router.router, prefix='/products', tags=['products']
)
app.include_router(orders_router.router, prefix='/orders', tags=['orders'])
app.include_router(payments_router.router, prefix='/payments', tags=['payments'])
app.include_router(auth_router.router, prefix='/auth', tags=['auth'])



@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Tech Challenge FIAP - Kauan Silva!'}
