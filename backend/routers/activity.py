"""활동 API 엔드포인트."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/activities", tags=["activities"])


@router.get("/categories")
def get_categories():
    """활동 카테고리 목록을 조회한다."""
    # TODO: US-002 구현
    pass


@router.post("/")
def create_activity():
    """새 활동(모임)을 생성한다."""
    # TODO: US-002 구현
    pass
