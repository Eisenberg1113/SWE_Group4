# 📱 Project Gachi: Community Platform for Students

## 1. Project Definition

**Gachi**는 대학 생활의 흩어진 정보를 한데 모으고, 학생 간의 신뢰 기반 소통을 지원하는 **RESTful API 기반 모바일 커뮤니티 플랫폼**입니다. 기존의 복잡한 커뮤니티 구조를 탈피하여, 자원(Resource) 중심의 깔끔한 설계와 현대적인 기술 스택(Kotlin, FastAPI)을 통해 구현됩니다.

---

## 2. Vision Statement

> **"연결의 가치를 더하다, Gachi"**
> 파편화된 대학 커뮤니티 환경에서 기술적 표준(REST)을 통해 데이터의 흐름을 투명하게 관리하고, 사용자에게는 '함께하는 가치'를 전달하는 가장 안정적이고 직관적인 소통 창구를 제공한다.

---

## 3. Project Goals & Scope

### **Project Goals**

* **Engineering**: RESTful API 설계 원칙을 준수하여 프론트엔드와 백엔드 간의 느슨한 결합(Loose Coupling) 실현.
* **Quality**: Kotlin의 Null-safety 기능을 활용하여 런타임 오류가 최소화된 안정적인 앱 환경 구축.
* **Documentation**: Swagger를 통한 API 명세 자동화로 협업 효율성 200% 달성.

### **Project Scope**

* **Backend**: Python FastAPI를 이용한 CRUD 로직 및 JWT 기반 인증 시스템 구축.
* **Mobile App**: Android Kotlin 기반의 네이티브 UI 및 Retrofit2를 이용한 실시간 데이터 연동.
* **Core Features**: 회원가입/로그인, 게시글 작성/수정/삭제, 댓글 시스템, 해시태그 기반 검색.

---

## 4. Stakeholders & Users

| 구분 | 대상 | 역할 및 기대효과 |
| --- | --- | --- |
| **Stakeholders** | **프로젝트 팀원** | 최신 스택(Kotlin, FastAPI) 숙련도 향상 및 SDLC 경험 |
|  | **담당 교수님** | 소프트웨어공학 원칙(REST, 설계 패턴) 준수 여부 평가 |
| **Target Users** | **대학생 (Main)** | 전공 정보 공유, 중고 물품 거래, 일상 소통 수행 |
|  | **커뮤니티 관리자** | 부적절한 게시물 모니터링 및 사용자 관리 기능 활용 |

---

## 5. Milestone (6주 집중 프로세스)

1. **Week 1: Requirements & Design**
* 요구사항 정의서 작성 및 ERD 설계
* REST API 엔드포인트 초안 확정


2. **Week 2-3: Core Development (Sprint 1)**
* FastAPI 기본 서버 및 DB 연동
* Kotlin 앱 기본 UI 프레임워크 구축


3. **Week 4: Feature Integration (Sprint 2)**
* API-App 데이터 연동 (Retrofit2)
* 로그인 및 게시판 CRUD 기능 완성


4. **Week 5: QA & Testing**
* Postman을 이용한 API 단위 테스트
* 앱 UI/UX 디버깅 및 예외 처리


5. **Week 6: Final Review & Deploy**
* GitHub 최종 정리 및 프로젝트 발표 자료 준비



---

## 6. GitHub Address

* **Repository**: https://github.com/Eisenberg1113/SWE_Group4
* **Branch Strategy**: `main` (배포), `develop` (개발), `feature/api` (기능별)

