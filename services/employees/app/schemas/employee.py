from pydantic import BaseModel
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    role: str
    salary: float

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeRead(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
