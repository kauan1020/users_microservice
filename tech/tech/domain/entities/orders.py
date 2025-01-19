from datetime import datetime
from enum import Enum
from typing import List, Optional

class OrderStatus(str, Enum):
    RECEIVED = 'RECEIVED'
    PREPARING = 'PREPARING'
    READY = 'READY'
    FINISHED = 'FINISHED'


class Order:
    def __init__(self, total_price: float, product_ids: List[int], status: OrderStatus, id: Optional[int] = None):
        self.id = id
        self.total_price = total_price
        self.product_ids = product_ids
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
