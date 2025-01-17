from datetime import datetime
from typing import Optional

class Products:
    def __init__(self, name: str, price: float, category: str, id: Optional[int] = None):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.created_at = datetime.now()
        self.updated_at = datetime.now()


