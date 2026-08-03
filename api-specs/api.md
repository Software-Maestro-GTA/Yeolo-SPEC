# API 명세 목록

이 문서는 Yeolo 프로젝트의 백엔드 서비스(FE-BE) 및 AI 엔진(BE-AI) 간의 API 요약 목록입니다. 상세한 호출 규격(Request/Response, JSON Schema, Error Codes)은 각 API ID 링크의 개별 문서에서 확인할 수 있습니다.

---

## 1. Frontend - Backend (FE-BE) API

| API ID | API 명 | HTTP Method | Endpoint |
| :--- | :--- | :--- | :--- |
| [API-AUTH-1](./API-AUTH-1.md) | Google OAuth 로그인 | `POST` | `/api/auth/google` |
| [API-AUTH-2](./API-AUTH-2.md) | Apple OAuth 로그인 | `POST` | `/api/auth/apple` |
| [API-AUTH-3](./API-AUTH-3.md) | 토큰 재발급 | `POST` | `/api/auth/refresh` |
| [API-AUTH-4](./API-AUTH-4.md) | 로그아웃 | `POST` | `/api/auth/logout` |
| [API-BOOKING-1](./API-BOOKING-1.md) | 예약 제휴 링크 조회 | `GET` | `/api/courses/{courseId}/booking-links` |
| [API-COURSE-1](./API-COURSE-1.md) | 여행 코스 생성 | `POST` | `/api/courses` |
| [API-COURSE-2](./API-COURSE-2.md) | 여행 코스 조회 | `GET` | `/api/courses/{courseId}` |
| [API-COURSE-3](./API-COURSE-3.md) | 여행 코스 목록 조회 | `GET` | `/api/courses` |
| [API-COURSE-4](./API-COURSE-4.md) | 여행 코스 삭제 | `DELETE` | `/api/courses/{courseId}` |
| [API-LOC-1](./API-LOC-1.md) | 국가 자동완성 조회 | `GET` | `/api/locations/countries/autocomplete` |
| [API-LOC-2](./API-LOC-2.md) | 도시 자동완성 조회 | `GET` | `/api/locations/cities/autocomplete` |
| [API-PLACE-1](./API-PLACE-1.md) | 여행 장소 조회 | `GET` | `/api/places/{placeId}` |
| [API-PREF-1](./API-PREF-1.md) | 사용자 MBTI 등록/수정 | `PATCH` | `/api/users/me/preferences` |
| [API-PREF-2](./API-PREF-2.md) | 사진 데이터 분석 동의 저장 | `POST` | `/api/users/me/consents/photo` |
| [API-PREF-3](./API-PREF-3.md) | 취향 분석 | `POST` | `/api/users/me/taste-profile/analysis` |
| [API-PREF-4](./API-PREF-4.md) | 취향 조회 | `GET` | `/api/users/me/taste-profile` |
| [API-SHARE-1](./API-SHARE-1.md) | 여행 코스 공유 링크 생성 | `POST` | `/api/courses/{courseId}/share-links` |
| [API-SHARE-2](./API-SHARE-2.md) | 여행 코스 공유 링크 조회 | `GET` | `/api/share-links/{shareToken}` |
| [API-SHARE-3](./API-SHARE-3.md) | 여행 코스 공유 링크 수락 | `POST` | `/api/share-links/{shareToken}/accept` |
| [API-USER-1](./API-USER-1.md) | 사용자 프로필 등록/수정 | `PATCH` | `/api/users/me/profile` |
| [API-USER-2](./API-USER-2.md) | 회원탈퇴 | `DELETE` | `/api/users/me` |

---

## 2. Backend - AI (BE-AI) 내부 API

| API ID | API 명 | HTTP Method | Endpoint |
| :--- | :--- | :--- | :--- |
| [API-AI-1](./API-AI-1.md) | 취향 분석 | `POST` | `/internal/ai/taste-profile/analysis` |
| [API-AI-2](./API-AI-2.md) | 여행 코스 생성 | `POST` | `/internal/ai/courses` |
