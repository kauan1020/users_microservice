from pydantic import BaseModel, ConfigDict
from typing import Literal

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