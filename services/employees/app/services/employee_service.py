from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from models.employee import Employee
from schemas.employee import EmployeeCreate
from typing import List


class EmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name(self, name: str) -> Employee:
            result = await self.db.execute(select(Employee).where(Employee.name == name))
            return result.scalars().first()

    async def get_by_id(self, employee_id: int) -> Employee:
        result = await self.db.execute(select(Employee).where(Employee.id == employee_id))
        employee = result.scalars().first()
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Employee not found.")
        return employee

    async def add(self, employee: Employee) -> Employee:
        self.db.add(employee)
        await self.db.commit()
        await self.db.refresh(employee)
        return employee

    async def list_all(self) -> List[Employee]:
        result = await self.db.execute(select(Employee))
        return result.scalars().all()

class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    async def create_employee(self, employee_data: EmployeeCreate) -> Employee:
        existing = await self.repository.get_by_name(employee_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Employee already exists."
            )
        employee = Employee(**employee_data.dict())
        return await self.repository.add(employee)

    async def list_employees(self) -> List[Employee]:
        return await self.repository.list_all()

    async def get_employee_by_id(self, employee_id: int) -> Employee:
        return await self.repository.get_by_id(employee_id)

    async def list_employees(self) -> List[Employee]:
        return await self.repository.list_all()
