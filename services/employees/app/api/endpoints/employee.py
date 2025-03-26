from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.employee import EmployeeCreate, EmployeeRead
from services.employee_service import EmployeeService, EmployeeRepository
from database import async_session

router = APIRouter()

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

def get_employee_service(db: AsyncSession = Depends(get_db)) -> EmployeeService:
    repository = EmployeeRepository(db)
    return EmployeeService(repository)

@router.post("/", response_model=EmployeeRead)
async def create_employee(employee_data: EmployeeCreate, service: EmployeeService = Depends(get_employee_service)):
    return await service.create_employee(employee_data)

@router.get("/", response_model=list[EmployeeRead])
async def list_employees(service: EmployeeService = Depends(get_employee_service)):
    return await service.list_employees()

@router.get("/{id}", response_model=EmployeeRead)
async def get_employee(id: int, service: EmployeeService = Depends(get_employee_service)):
    return await service.get_employee_by_id(id)
