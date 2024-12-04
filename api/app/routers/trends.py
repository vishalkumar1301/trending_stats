from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..models.trend import TrendCreate, TrendInDB
from typing import List
from bson import ObjectId
from ..database.mongodb import get_database

router = APIRouter()

@router.post("/trends/", response_model=TrendInDB)
async def create_trend(trend: TrendCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    trend_dict = trend.model_dump()
    trend_dict["_id"] = str(ObjectId())
    await db.trends.insert_one(trend_dict)
    return TrendInDB(**trend_dict)

@router.get("/trends/", response_model=List[TrendInDB])
async def read_trends(skip: int = 0, limit: int = 10, db: AsyncIOMotorDatabase = Depends(get_database)):
    trends = await db.trends.find().skip(skip).limit(limit).to_list(length=limit)
    return [TrendInDB(**trend) for trend in trends]

@router.get("/trends/{trend_id}", response_model=TrendInDB)
async def read_trend(trend_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    if (trend := await db.trends.find_one({"_id": trend_id})) is not None:
        return TrendInDB(**trend)
    raise HTTPException(status_code=404, detail="Trend not found")

@router.put("/trends/{trend_id}", response_model=TrendInDB)
async def update_trend(trend_id: str, trend: TrendCreate, db: AsyncIOMotorDatabase = Depends(get_database)):
    update_result = await db.trends.update_one(
        {"_id": trend_id}, {"$set": trend.model_dump()}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Trend not found")
    return TrendInDB(**{**trend.model_dump(), "_id": trend_id})

@router.delete("/trends/{trend_id}")
async def delete_trend(trend_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    delete_result = await db.trends.delete_one({"_id": trend_id})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Trend not found")
    return {"message": "Trend deleted successfully"} 