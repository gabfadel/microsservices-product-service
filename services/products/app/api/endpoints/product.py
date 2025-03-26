from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.product import ProductCreate, ProductRead
from services.product_service import ProductService, ProductRepository
from database import async_session

router = APIRouter()

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    repository = ProductRepository(db)
    return ProductService(repository)

@router.post("/", response_model=ProductRead)
async def create_product(product_data: ProductCreate, service: ProductService = Depends(get_product_service)):
    return await service.create_product(product_data)

@router.get("/", response_model=list[ProductRead])
async def list_products(service: ProductService = Depends(get_product_service)):
    return await service.list_products()

@router.get("/{id}", response_model=ProductRead)
async def get_product(id: int, service: ProductService = Depends(get_product_service)):
    return await service.get_product_by_id(id)
