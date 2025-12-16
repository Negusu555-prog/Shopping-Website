from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import database
from Controller import user_controller, product_controller, order_controller, favorite_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(
    title="Shopping Website API",
    description="AI-powered shopping website backend",
    version="1.0.0",
    lifespan=lifespan
)

# הוספת כל ה-routers
app.include_router(user_controller.router)
app.include_router(product_controller.router)
app.include_router(order_controller.router)
app.include_router(favorite_controller.router)

@app.get("/")
async def root():
    return {"message": "Shopping Website API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}