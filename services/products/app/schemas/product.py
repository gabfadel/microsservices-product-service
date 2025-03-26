from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    
class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

    class Config:
        orm_mode = True
