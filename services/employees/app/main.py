from fastapi import FastAPI
from api.endpoints import employee
from database import init_db

app = FastAPI(title="Employees Service")

app.include_router(employee.router, prefix="/employees", tags=["employees"])

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Employees Service is active!"}
