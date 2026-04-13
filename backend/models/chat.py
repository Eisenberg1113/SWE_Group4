"""채팅 모델."""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.sql import func

from database import Base


class ChatRoom(Base):
    """채팅방 테이블."""

    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Message(Base):
    """메시지 테이블."""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"), nullable=False)
    sender_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, server_default=func.now())
