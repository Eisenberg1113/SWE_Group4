# SWE_Group4
Software Engineering Group Project


# 📱 Gachi (가치): 대학생 전용 커뮤니티 플랫폼


## 📝 프로젝트 개요

* **서비스 명칭**: Gachi (가치)
* **슬로건**: "우리 동네, 우리 학교의 가치를 잇다"
* **핵심 목표**:
* **Modern Tech**: Java 기반의 구형 설계를 탈피하여 Kotlin과 Python의 생산성 극대화.
* **RESTful Standard**: 표준 HTTP Method와 상태 코드를 활용한 정석적인 API 설계.
* **User Experience**: 비동기 통신을 통한 끊김 없는 커뮤니티 경험 제공.



---

## 🛠 Tech Stack

| 분류 | 기술 스택 | 상세 내용 |
| --- | --- | --- |
| **Frontend** | **Android (Kotlin)** | 신규 네이티브 앱 개발 |
| **Backend** | **Python (FastAPI)** | 비동기 기반 고성능 REST API 서버 |
| **Database** | **SQLite** | 관계형 데이터베이스 (RDBMS) |
| **Network** | **Retrofit2** | Type-safe한 HTTP 클라이언트 라이브러리 |
| **Serialization** | **Pydantic / Gson** | JSON 데이터 직렬화 및 검증 |

---

## 🏗 시스템 아키텍처 (System Architecture)

Gachi 플랫폼은 클라이언트(Kotlin)와 서버(FastAPI)가 분리된 구조로, JSON 포맷을 통해 데이터를 교환합니다.

---

## 🗺 REST API 설계 (Gachi Resource Design)

리소스 중심의 URI 설계를 통해 직관적이고 유지보수가 쉬운 API를 제공합니다.

| 도메인 | Method | 엔드포인트 | 설명 |
| --- | --- | --- | --- |
| **게시글** | `GET` | `/posts` | 전체 게시글 목록 조회 |
|  | `POST` | `/posts` | 새로운 게시글 작성 |
|  | `GET` | `/posts/{id}` | 특정 게시글 상세 보기 |
|  | `DELETE` | `/posts/{id}` | 본인 게시글 삭제 |
| **댓글** | `POST` | `/posts/{id}/comments` | 특정 게시글에 댓글 작성 |
| **사용자** | `POST` | `/auth/register` | 신규 회원가입 |
|  | `POST` | `/auth/login` | 로그인 및 액세스 토큰 발급 |

---

## 🛡 소프트웨어공학적 설계 포인트

1. **Strict RESTful API**: 동사형 URL(`getPost`)을 배제하고 명사형 자원(`posts`)과 HTTP Method(`GET`, `POST`)를 조합하여 설계했습니다.
2. **Schema Validation**: Python의 `Pydantic`과 Kotlin의 `Data Class`를 매핑하여 클라이언트-서버 간 데이터 규격을 엄격히 관리합니다.
3. **Scalable DB Schema**: 유저와 게시글, 댓글 간의 관계를 정규화하여 데이터 무결성을 보장합니다.

---

## 👥 팀원 역할

* A (Android/Kotlin)**: Gachi 앱 UI 개발 및 Retrofit 기반 API 연동
* B (Backend/Python)**: FastAPI 서버 아키텍처 설계 및 DB 스키마 구현
* C (Project Manager)**: API 명세서 작성(Swagger) 및 소프트웨어 요구사항 정의서 관리

---

🌟 Project Vision & Goals
Project Vision
"단순한 소통을 넘어, 파편화된 대학 생활의 정보를 하나로 잇는 가치 있는 연결"

Gachi는 대학생들이 겪는 정보의 불균형을 해소하고, 신뢰할 수 있는 기술 스택을 통해 누구나 쉽고 안전하게 참여할 수 있는 커뮤니티 생태계를 지향합니다.

Project Goals
기술적 도전 (Technical Excellence)

RESTful API의 정석 구현: 리소스 중심의 설계와 적절한 HTTP 상태 코드 활용으로 표준화된 백엔드 구축.

Modern Android: Kotlin의 최신 기능을 활용하여 안정적이고 반응성 높은 UI/UX 제공.

Loose Coupling: 프론트엔드와 백엔드의 완전한 분리를 통해 독립적인 개발 및 배포 환경 체득.

사용자 경험 (User Experience)

데이터 기반 소통: 게시글, 댓글, 좋아요 등 핵심 커뮤니티 기능을 통해 사용자 간 상호작용 극대화.

직관적인 인터페이스: 복잡한 기능보다는 사용자에게 꼭 필요한 핵심 기능 중심의 미니멀리즘 UI 구현.

공학적 프로세스 (Engineering Process)

협업의 가치: Git Flow와 Issue 기반의 협업을 통해 체계적인 소프트웨어 개발 생명주기(SDLC) 경험.

문서화의 자동화: Swagger를 이용한 API 명세 자동화로 팀원 간 커뮤니케이션 비용 최소화.
