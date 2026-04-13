"""Gachi API 서버 진입점."""

from fastapi import FastAPI

app = FastAPI(
    title="Gachi API",
    description="익명 활동 매칭 서비스 API",
    version="0.1.0",
)


@app.get("/")
def root():
    """헬스 체크 엔드포인트."""
    return {"status": "ok", "service": "gachi-api"}
