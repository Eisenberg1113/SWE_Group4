"""인증 API 엔드포인트."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
def register():
    """일회용 익명 계정을 발급한다."""
    # TODO: US-001 구현
    pass


@router.post("/login")
def login():
    """발급된 ID/PW로 로그인한다."""
    # TODO: US-001 구현
    pass
