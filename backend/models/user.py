"""사용자 모델."""

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func

from database import Base


class User(Base):
    """일회용 익명 사용자 테이블."""

    __tablename__ = "users"

    id = Column(String(36), primary_key=True)
    anonymous_id = Column(String(20), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=False)
