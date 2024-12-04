from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from .core.config import settings
from .routers import trends

app = FastAPI(
    title="Trending Statistics API",
    description="API for accessing trending statistics from CrewAI",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client[settings.MONGODB_DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(trends.router, prefix="/api/v1", tags=["trends"])

@app.get("/")
async def root():
    return {"message": "Welcome to Trending Statistics API"} 