"""관리자 API 엔드포인트."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/blocked-words")
def get_blocked_words():
    """차단 키워드 목록을 조회한다."""
    # TODO: AD-001 구현
    pass


@router.get("/sessions")
def get_active_sessions():
    """활성 세션 목록을 조회한다."""
    # TODO: AD-002 구현
    pass


@router.get("/activities/monitor")
def get_activity_monitor():
    """모임 모니터링 데이터를 조회한다."""
    # TODO: AD-003 구현
    pass


@router.get("/statistics")
def get_statistics():
    """카테고리별 활동 통계를 조회한다."""
    # TODO: AD-004 구현
    pass
