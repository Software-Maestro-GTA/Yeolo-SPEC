# [API-AUTH-3] 토큰 재발급

## 1. 기본 정보

- **Method**: `POST`
- **Endpoint**: `/api/auth/refresh`
- **통신 방식**: REST
- **인증 필요**: N
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Authorization": "Bearer {refreshToken}",
  "Content-Type": "application/json"
}

### Request Body
```json
{
  "refreshToken": "string"
}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "토큰 재발급 성공",
  "data": {
    "accessToken": "string",
    "refreshToken": "string"
  }
}
```

### Error Codes
401: refresh token 만료/무효
500: 서버 오류

### 실패 응답
```json
{
  "status": 401,
  "message": "Refresh Token이 유효하지 않거나 만료되었습니다.",
  "data": null
}
```

