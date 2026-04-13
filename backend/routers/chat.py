"""채팅 API 엔드포인트."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.get("/rooms/{room_id}/messages")
def get_messages(room_id: int):
    """채팅방 메시지 목록을 조회한다."""
    # TODO: US-005 구현
    pass
