# 🎓 Gachi — 캠퍼스 익명 활동 매칭 서비스 결과 보고서

> **프로젝트명**: Gachi  
> **작성일**: 2026년 4월 29일  
> **기술 스택**: Django + PostgreSQL + Nginx + Docker Compose

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 서비스명 | **Gachi** — 캠퍼스 익명 취미 매칭 서비스 |
| 핵심 기능 | Google OAuth 로그인, 모임 생성/매칭, 인앱 채팅, 매너온도, 관리자 대시보드 |
| 대상 사용자 | 대학생 (User), 운영 관리자 (Admin) |
| 인증 방식 | Google OAuth 2.0 (`django-allauth`) — 닉네임만 타 유저에게 노출 |
| 접속 URL | `http://localhost` (Docker Compose 실행 후) |

---

## 2. 시스템 아키텍처

