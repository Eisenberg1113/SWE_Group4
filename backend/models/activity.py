"""활동 모델."""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from database import Base


class Category(Base):
    """활동 카테고리 테이블."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    icon = Column(String(50), nullable=True)


class Activity(Base):
    """활동(모임) 테이블."""

    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    creator_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    location_lat = Column(String(20), nullable=True)
    location_lng = Column(String(20), nullable=True)
    location_address = Column(String(255), nullable=True)
    scheduled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
