from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING


class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    role: str
    salary: float
