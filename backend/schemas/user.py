"""사용자 관련 요청/응답 스키마."""

from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    """일회용 계정 생성 응답."""

    anonymous_id: str
    password: str


class UserLogin(BaseModel):
    """로그인 요청."""

    anonymous_id: str
    password: str


class TokenResponse(BaseModel):
    """JWT 토큰 응답."""

    access_token: str
    token_type: str = "bearer"
    expires_at: datetime
