from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Literal


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    cpf: str


class UserDB(UserSchema):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class ProductSchema(BaseModel):
    name: str
    price: float
    category: Literal['Lanche', 'Acompanhamento', 'Bebida', 'Sobremesa']


class ProductPublic(BaseModel):
    id: int
    name: str
    price: float
    category: str
    model_config = ConfigDict(from_attributes=True)


class OrderStatusEnum(str, Enum):
    RECEIVED = 'Recebido'
    PREPARING = 'Em preparação'
    READY = 'Pronto'
    FINISHED = 'Finalizado'


class OrderCreate(BaseModel):
    product_ids: list[int]


class OrderUpdate(BaseModel):
    status: OrderStatusEnum


class ProductDetail(BaseModel):
    id: int
    name: str
    price: float


class OrderPublic(BaseModel):
    id: int
    total_price: float
    status: str
    products: list[ProductDetail]

    class Config:
        orm_mode = True


class OrderList(BaseModel):
    orders: list[OrderPublic]
