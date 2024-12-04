from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

class TrendBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    source: Optional[str] = None
    data: Any
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TrendCreate(TrendBase):
    pass

class TrendInDB(TrendBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "title": "Tech Trends 2024",
                "description": "Analysis of tech trends",
                "category": "Technology",
                "source": "CrewAI Analysis",
                "data": {},
                "created_at": "2024-01-20T00:00:00",
                "updated_at": "2024-01-20T00:00:00"
            }
        } 