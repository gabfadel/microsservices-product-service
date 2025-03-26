from sqlmodel import SQLModel, Field, Relationship
from typing import Optional,TYPE_CHECKING

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    stock: int
