# API 명세 목록

이 문서는 Yeolo 프로젝트의 백엔드 서비스(FE-BE) 및 AI 엔진(BE-AI) 간의 API 요약 목록입니다. 상세한 호출 규격(Request/Response, JSON Schema, Error Codes)은 각 API ID 링크의 개별 문서에서 확인할 수 있습니다.

---

## 1. Frontend - Backend (FE-BE) API

| API ID                      | API 명                                | HTTP Method | Endpoint                      |
| :-------------------------- | :------------------------------------ | :---------- | :---------------------------- |
| [API-FB-1](./API-FB-1.md)   | Google OAuth 로그인                   | `POST`      | `/api/auth/google`            |
| [API-FB-2](./API-FB-2.md)   | 이미지 메타데이터 기반 성향 분석 생성 | `POST`      | `/api/taste-profile/behavior` |
| [API-FB-3](./API-FB-3.md)   | 최소 설문 기반 성향 분석 생성         | `POST`      | `/api/taste-profile/survey`   |
| [API-FB-4](./API-FB-4.md)   | 개인 맞춤형 여행 코스 생성            | `POST`      | `/api/courses`                |
| [API-FB-7](./API-FB-7.md)   | 여행 코스 상세 조회                   | `GET`       | `/api/courses/{courseId}`     |
| [API-FB-8](./API-FB-8.md)   | 내 성향 프로필 조회                   | `GET`       | `/api/me/taste-profile`       |
| [API-FB-10](./API-FB-10.md) | 이전 생성 코스 목록 조회              | `GET`       | `/api/courses`                |
| [API-FB-11](./API-FB-11.md) | 로그아웃                              | `POST`      | `/api/auth/logout`            |
| [API-FB-12](./API-FB-12.md) | 회원탈퇴                              | `DELETE`    | `/api/users/me`               |

---

## 2. Backend - AI (BE-AI) 내부 API

| API ID                    | API 명                                  | HTTP Method | Endpoint                              |
| :------------------------ | :-------------------------------------- | :---------- | :------------------------------------ |
| [API-BA-1](./API-BA-1.md) | 성향 프로필 기반 여행 코스 생성         | `POST`      | `/internal/ai/courses`                |
| [API-BA-6](./API-BA-6.md) | 전처리 이미지 메타데이터 기반 성향 분석 | `POST`      | `/internal/ai/taste-profile/behavior` |
