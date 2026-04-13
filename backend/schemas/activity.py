"""활동 관련 요청/응답 스키마."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ActivityCreate(BaseModel):
    """활동 생성 요청."""

    category_id: int
    location_lat: Optional[str] = None
    location_lng: Optional[str] = None
    location_address: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class ActivityResponse(BaseModel):
    """활동 응답."""

    id: int
    category_id: int
    creator_id: str
    location_address: Optional[str]
    scheduled_at: Optional[datetime]
    created_at: datetime

    class Config:
        """ORM 모드 활성화."""

        from_attributes = True
