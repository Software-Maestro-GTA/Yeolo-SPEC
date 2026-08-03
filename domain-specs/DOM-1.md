# [DOM-1] 사용자 정보

## 사용자 정보

OAuth 로그인을 통해 생성되는 서비스 내부 사용자 정보를 저장하는 도메인이다.

사용자 정보는 로그인, 프로필 수정, 취향 정보/코스 정보 소유자 연결, 친구 초대, 마이페이지 표시의 기준 데이터로 사용된다.


## 저장 목적

- Google OAuth 또는 Apple OAuth 로그인 사용자를 식별한다.
- 내부 사용자 계정을 생성하거나 기존 계정을 조회한다.
- 취향 정보, 코스 정보, 동의 정보와 `userId` 기준으로 연결한다.
- 로그인 세션 발급 및 마지막 로그인 시각 관리에 사용한다.
- 마이페이지와 프로필 수정 화면에 필요한 기본 사용자 정보를 제공한다.

## 주요 필드

| 필드 | 타입 | 설명 |
| :--- | :--- | :--- |
| `userId` | UUID | 서비스 내부 사용자 고유 식별자 |
| `provider` | string | OAuth 제공자 |
| `providerUserId` | string | OAuth 제공자가 발급한 외부 사용자 고유 식별자 |
| `email` | nullable string | 사용자 이메일 |
| `displayName` | nullable string | 사용자 표시 이름 |
| `profileImageUrl` | nullable string | 사용자 프로필 이미지 URL |
| `status` | string | 사용자 계정 상태 |
| `createdAt` | string(ISO-8601) | 최초 가입 시각 |
| `lastLoginAt` | string(ISO-8601) | 마지막 로그인 시각 |
| `deletedAt` | nullable string(ISO-8601) | 탈퇴 또는 비활성화 시각 |


## 필드 설명


### `provider`

현재 지원하는 로그인 제공자는 다음과 같다.

| 값 | 의미 |
| :--- | :--- |
| `google` | Google OAuth 로그인 |
| `apple` | Apple OAuth 로그인 |


### `status`

| 값 | 의미 |
| :--- | :--- |
| `active` | 정상 사용자 |
| `inactive` | 비활성 사용자 |
| `deleted` | 탈퇴 사용자 |


## 프로필 정보 처리 기준

- `email`, `displayName`, `profileImageUrl`은 모두 `null`일 수 있다.
- Apple OAuth의 경우 최초 동의 시점 외에는 이메일이나 이름이 제공되지 않을 수 있다.
- 사용자가 직접 프로필 이미지를 업로드하면 서버가 저장 후 `profileImageUrl`을 생성한다.
- 앱은 `email` 또는 `displayName`이 `null`이면 사용자 정보 등록/수정 화면으로 유도할 수 있다.

## 다른 도메인과의 관계

- `userId`는 취향 정보의 소유자 식별자로 사용된다.
- `userId`는 코스 정보의 생성자/소유자 식별자로 사용된다.
- MBTI는 사용자 선호 입력값으로 별도 관리되며, 사용자 정보 자체의 필드로 저장하지 않는다.
- 사진 데이터 분석 동의 정보도 별도 동의 도메인/정책으로 관리한다.

## 예시

```json
{
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "provider": "google",
  "providerUserId": "109876543210123456789",
  "email": "user@gmail.com",
  "displayName": "김선규",
  "profileImageUrl": "https://cdn.example.com/profile/user-1.png",
  "status": "active",
  "createdAt": "2026-07-13T06:00:00Z",
  "lastLoginAt": "2026-07-13T06:10:00Z",
  "deletedAt": null
}
```
