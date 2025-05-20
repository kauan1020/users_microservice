from http import HTTPStatus

from fastapi import FastAPI

from tech.api import  users_router, auth_router
from tech.interfaces.schemas.message_schema import (
    Message,
)


app = FastAPI()
app.include_router(users_router.router, prefix='/users', tags=['users'])

app.include_router(auth_router.router, prefix='/auth', tags=['auth'])



@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Tech Challenge FIAP - Kauan Silva!'
                       '    Users And Auth microservice'}
