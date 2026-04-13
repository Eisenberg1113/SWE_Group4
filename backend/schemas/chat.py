"""채팅 관련 요청/응답 스키마."""

from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    """메시지 전송 요청."""

    content: str


class MessageResponse(BaseModel):
    """메시지 응답."""

    id: int
    sender_id: str
    content: str
    sent_at: datetime

    class Config:
        """ORM 모드 활성화."""

        from_attributes = True
