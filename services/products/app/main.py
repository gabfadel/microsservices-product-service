from fastapi import FastAPI
from api.endpoints import product
from database import init_db

app = FastAPI(title="Products Service")

app.include_router(product.router, prefix="/products", tags=["products"])

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Products Service is active!"}
