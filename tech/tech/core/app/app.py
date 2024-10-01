from http import HTTPStatus

from fastapi import FastAPI


from tech.core.app import users_router, products_router
from tech.core.app import orders_router
from tech.core.domain.schemas import (
    Message,
)


app = FastAPI()
app.include_router(users_router.router, prefix='/users', tags=['users'])
app.include_router(
    products_router.router, prefix='/products', tags=['products']
)
app.include_router(orders_router.router, prefix='/orders', tags=['orders'])


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Tech Challenge FIAP - Kauan Silva!'}
