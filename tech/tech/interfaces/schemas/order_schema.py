from pydantic import BaseModel
from enum import Enum

class OrderStatusEnum(str, Enum):
    RECEIVED = 'RECEIVED'
    PREPARING = 'PREPARING'
    READY = 'READY'
    FINISHED = 'FINISHED'


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
    status: OrderStatusEnum
    products: list[ProductDetail]

    class Config:
        orm_mode = True


class OrderList(BaseModel):
    orders: list[OrderPublic]
