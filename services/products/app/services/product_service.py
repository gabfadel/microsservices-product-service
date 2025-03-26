from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from models.product import Product
from schemas.product import ProductCreate
from typing import List

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name(self, name: str) -> Product:
        result = await self.db.execute(select(Product).where(Product.name == name))
        return result.scalars().first()

    async def get_by_id(self, product_id: int) -> Product:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Product not found.")
        return product

    async def add(self, product: Product) -> Product:
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def list_all(self) -> List[Product]:
        result = await self.db.execute(select(Product))
        return result.scalars().all()

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def create_product(self, product_data: ProductCreate) -> Product:
        existing = await self.repository.get_by_name(product_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product already exists."
            )
        product = Product(**product_data.dict())
        return await self.repository.add(product)

    async def list_products(self) -> List[Product]:
        return await self.repository.list_all()

    async def get_product_by_id(self, product_id: int) -> Product:
        return await self.repository.get_by_id(product_id)
