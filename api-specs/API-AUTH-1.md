# [API-AUTH-1] Google OAuth 로그인

## 1. 기본 정보

- **Method**: `POST`
- **Endpoint**: `/api/auth/google`
- **통신 방식**: REST
- **인증 필요**: N
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Content-Type": "application/json"
}

### Request Body
```json
{
  "code": "string",
  "redirectUri": "string"
}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "로그인 성공",
  "data": {
    "user": {
      "userId": "string(UUID)",
      "provider": "google",
      "email": "string|null",
      "displayName": "string|null",
      "profileImageUrl": "string|null",
      "status": "active",
      "lastLoginAt": "string(ISO-8601)"
    },
    "doOnboarding": "boolean",
    "accessToken": "string",
    "refreshToken": "string"
  }
}
```

### Error Codes
400: 유효하지 않은 Google OAuth 요청/인가 코드
401: Google OAuth 인증 실패
500: 서버 오류

### 실패 응답
```json
{
  "status": 400,
  "message": "유효하지 않은 Google OAuth 인가 코드입니다.",
  "data": null
}
```

