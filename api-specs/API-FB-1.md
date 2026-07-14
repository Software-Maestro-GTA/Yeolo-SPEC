# [API-FB-1] Google OAuth 로그인

Google OAuth 인가 코드를 전달받아 사용자를 가입 또는 로그인 처리하고, 내부 세션 유지용 JWT Access/Refresh Token을 발급합니다.

---

## 1. API 개요

- **Endpoint**: `/api/auth/google`
- **Method**: `POST`
- **통신 방식**: `REST`
- **인증 필요**: `false`

---

## 2. Request 사양

### Body

```json
{
  "code": "string",
  "redirectUri": "string(optional)"
}
```

---

## 3. Response 사양

### 성공 응답 (Status 200)

```json
{
  "status": 200,
  "message": "로그인 성공",
  "data": {
    "user": {
      "userId": "string(UUID)",
      "email": "string",
      "nickname": "string",
      "profileImage": "string",
      "hasTasteProfile": "boolean"
    },
    "accessToken": "string",
    "refreshToken": "string"
  }
}
```

---

## 4. 에러 코드 및 예외 처리

- **400**: Google 인가 코드 누락/만료/형식 오류
- **500**: Google 인증 서버 장애 및 내부 처리 오류

### 실패 응답 (Status 400)

```json
{
  "status": 400,
  "message": "인가 코드가 유효하지 않습니다.",
  "data": null
}
```
