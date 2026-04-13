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
