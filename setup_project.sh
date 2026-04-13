#!/bin/bash
# ============================================
# Gachi Project - Directory Structure Setup
# SWE_Group4
# ============================================

echo "📁 Gachi 프로젝트 디렉토리 구조를 생성합니다..."

# Backend - FastAPI
mkdir -p backend/models
mkdir -p backend/schemas
mkdir -p backend/routers
mkdir -p backend/services
mkdir -p backend/tests

# Android - Kotlin
mkdir -p android/ui
mkdir -p android/api
mkdir -p android/model
mkdir -p android/util

# Admin Web - Dashboard
mkdir -p admin-web/css
mkdir -p admin-web/js

# Docs
mkdir -p docs

# ============================================
# .gitkeep 파일 생성 (빈 폴더도 Git에 추적)
# ============================================
find . -type d -empty -not -path './.git/*' -exec touch {}/.gitkeep \;

# ============================================
# Backend 기본 파일 생성
# ============================================

# main.py - FastAPI 진입점
cat > backend/main.py << 'EOF'
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
EOF

# config.py - 설정
cat > backend/config.py << 'EOF'
"""애플리케이션 설정."""

import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:password@localhost:3306/gachi"
)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60
EOF

# database.py - DB 연결
cat > backend/database.py << 'EOF'
"""MySQL 데이터베이스 연결 설정."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """DB 세션 의존성 주입."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
EOF

# Models
cat > backend/models/__init__.py << 'EOF'
"""데이터베이스 모델 패키지."""
EOF

cat > backend/models/user.py << 'EOF'
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
EOF

cat > backend/models/activity.py << 'EOF'
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
EOF

cat > backend/models/chat.py << 'EOF'
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
EOF

# Schemas
cat > backend/schemas/__init__.py << 'EOF'
"""Pydantic 스키마 패키지."""
EOF

cat > backend/schemas/user.py << 'EOF'
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
EOF

cat > backend/schemas/activity.py << 'EOF'
"""활동 관련 요청/응답 스키마."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ActivityCreate(BaseModel):
    """활동 생성 요청."""

    category_id: int
    location_lat: Optional[str] = None
    location_lng: Optional[str] = None
    location_address: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class ActivityResponse(BaseModel):
    """활동 응답."""

    id: int
    category_id: int
    creator_id: str
    location_address: Optional[str]
    scheduled_at: Optional[datetime]
    created_at: datetime

    class Config:
        """ORM 모드 활성화."""

        from_attributes = True
EOF

cat > backend/schemas/chat.py << 'EOF'
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
EOF

# Routers
cat > backend/routers/__init__.py << 'EOF'
"""API 라우터 패키지."""
EOF

cat > backend/routers/auth.py << 'EOF'
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
EOF

cat > backend/routers/activity.py << 'EOF'
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
EOF

cat > backend/routers/chat.py << 'EOF'
"""채팅 API 엔드포인트."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.get("/rooms/{room_id}/messages")
def get_messages(room_id: int):
    """채팅방 메시지 목록을 조회한다."""
    # TODO: US-005 구현
    pass
EOF

cat > backend/routers/admin.py << 'EOF'
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
EOF

# Services
cat > backend/services/__init__.py << 'EOF'
"""비즈니스 로직 서비스 패키지."""
EOF

cat > backend/services/auth_service.py << 'EOF'
"""인증 서비스 로직."""

# TODO: JWT 토큰 생성, 일회용 계정 발급 로직
EOF

cat > backend/services/matching_service.py << 'EOF'
"""매칭 서비스 로직."""

# TODO: 카테고리 기반 매칭 알고리즘
EOF

cat > backend/services/chat_service.py << 'EOF'
"""채팅 서비스 로직."""

# TODO: WebSocket 실시간 채팅 관리
EOF

# Tests
cat > backend/tests/__init__.py << 'EOF'
"""테스트 패키지."""
EOF

# ============================================
# Admin Web 기본 파일
# ============================================

cat > admin-web/index.html << 'EOF'
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gachi Admin Dashboard</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <h1>Gachi 관리자 대시보드</h1>
    <p>준비 중입니다.</p>
    <script src="js/main.js"></script>
</body>
</html>
EOF

cat > admin-web/css/style.css << 'EOF'
/* Gachi Admin Dashboard 스타일 */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background-color: #f5f5f5;
    color: #333;
    padding: 2rem;
}
EOF

cat > admin-web/js/main.js << 'EOF'
// Gachi Admin Dashboard 메인 스크립트

console.log("Gachi Admin Dashboard loaded");
EOF

# ============================================
# requirements.txt
# ============================================

cat > requirements.txt << 'EOF'
fastapi==0.111.0
uvicorn==0.30.1
sqlalchemy==2.0.31
pymysql==1.1.1
pydantic==2.8.2
python-jose==3.3.0
passlib==1.7.4
websockets==12.0
EOF

# ============================================
# .gitignore
# ============================================

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.egg-info/
venv/
.env

# Android
*.apk
*.aab
.gradle/
build/
local.properties

# IDE
.idea/
.vscode/
*.iml

# OS
.DS_Store
Thumbs.db
EOF

echo ""
echo "✅ 프로젝트 디렉토리 구조 생성 완료!"
echo ""
echo "📂 생성된 구조:"
find . -not -path './.git/*' -not -name '.git' | head -60 | sed 's/[^/]*\//  /g'
echo ""
echo "🚀 다음 단계:"
echo "   1. git add -A"
echo "   2. git commit -m 'chore: 프로젝트 디렉토리 구조 초기화'"
echo "   3. git push origin main"
