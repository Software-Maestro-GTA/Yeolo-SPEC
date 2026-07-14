# [DOM-3] 사용자 정보 (User)

Google OAuth 기반 로그인 사용자를 식별하고, 성향 프로필·행동 데이터·추천 코스의 소유자를 연결하기 위한 도메인입니다.

---

## 1. 주요 필드 정의

- `userId`: 서비스 내부 사용자 고유 식별자 (UUID)
- `provider`: OAuth 제공자 (예: `google`)
- `providerUserId`: Google OAuth에서 제공하는 사용자 고유 식별자 (`sub`)
- `email`: 사용자 이메일
- `displayName`: 사용자 표시 이름
- `profileImageUrl`: 사용자 프로필 이미지 URL
- `status`: 사용자 계정 상태
- `createdAt`: 최초 가입 시각
- `lastLoginAt`: 마지막 로그인 시각
- `deletedAt`: 탈퇴 또는 비활성화 시각

---

## 2. 저장 목적

- Google OAuth 로그인 후 내부 사용자 계정을 생성하거나 조회한다.
- 성향 정보, 행동 데이터, 코스 정보의 `user_id`와 연결한다.
- 로그인 세션 발급, 사용자 식별, 개인화 추천 요청의 기준 데이터로 사용한다.

---

## 3. Enum 정의

| 필드       | 저장값     | 표시/의미           |
| :--------- | :--------- | :------------------ |
| `provider` | `google`   | Google OAuth 로그인 |
| `status`   | `active`   | 정상 사용자         |
| `status`   | `inactive` | 비활성 사용자       |
| `status`   | `deleted`  | 탈퇴 사용자         |

---

## 4. 데이터베이스 컬럼 스펙

| 컬럼                        | 타입        | 역할                                        |
| :-------------------------- | :---------- | :------------------------------------------ |
| `id`                        | UUID        | 사용자 PK                                   |
| `provider`                  | TEXT        | OAuth 제공자                                |
| `provider_user_id`          | TEXT        | OAuth 제공자 기준 사용자 ID — Google `sub`  |
| `email`                     | TEXT        | 사용자 이메일                               |
| `display_name`              | TEXT        | 사용자 표시 이름                            |
| `profile_image_url`         | TEXT        | 프로필 이미지 URL                           |
| `status`                    | TEXT        | 계정 상태 — `active`, `inactive`, `deleted` |
| `created_at` / `updated_at` | TIMESTAMPTZ | 생성·수정 시각                              |
| `last_login_at`             | TIMESTAMPTZ | 마지막 로그인 시각                          |
| `deleted_at`                | TIMESTAMPTZ | 탈퇴 또는 삭제 시각                         |

---

## 5. JSON 예시

```json
{
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "provider": "google",
  "providerUserId": "109876543210123456789",
  "email": "user@gmail.com",
  "displayName": "김선규",
  "profileImageUrl": "https://lh3.googleusercontent.com/...",
  "status": "active",
  "createdAt": "2026-07-13T06:00:00Z",
  "lastLoginAt": "2026-07-13T06:10:00Z",
  "deletedAt": null
}
```
