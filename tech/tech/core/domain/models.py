
from datetime import datetime
from enum import Enum
from typing import List, Optional
from tech.core.domain.value_objects import CPF


class OrderStatus(str, Enum):
    RECEIVED = 'RECEIVED'
    PREPARING = 'PREPARING'
    READY = 'READY'
    FINISHED = 'FINISHED'


class User:
    def __init__(self, username: str, password: str, cpf: CPF, email: str, id: Optional[int] = None):
        self.id = id
        self.username = username
        self.password = password
        self.cpf = cpf
        self.email = email
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update_password(self, new_password: str):
        self.password = new_password
        self.updated_at = datetime.now()

    def update_email(self, new_email: str):
        self.email = new_email
        self.updated_at = datetime.now()


class Products:
    def __init__(self, name: str, price: float, category: str, id: Optional[int] = None):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


class Order:
    def __init__(self, total_price: float, product_ids: List[int], status: OrderStatus, id: Optional[int] = None):
        self.id = id
        self.total_price = total_price
        self.product_ids = product_ids
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
