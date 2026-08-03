# [API-USER-1] 사용자 프로필 등록/수정

## 1. 기본 정보

- **Method**: `PATCH`
- **Endpoint**: `/api/users/me/profile`
- **통신 방식**: REST
- **인증 필요**: Y
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Authorization": "Bearer {accessToken}",
  "Content-Type": "multipart/form-data"
}

### Request Body
```json
{
  "email": "string|null",
  "displayName": "string|null",
  "profileImage": "file|null"
}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "사용자 프로필 수정 성공",
  "data": {
    "user": {
      "userId": "string(UUID)",
      "provider": "google | apple",
      "email": "string|null",
      "displayName": "string|null",
      "profileImageUrl": "string|null",
      "status": "active",
      "lastLoginAt": "string(ISO-8601)"
    }
  }
}
```

### Error Codes
400: 잘못된 입력값
401: 인증 실패
409: 이미 사용 중인 이메일
413: 프로필 이미지 용량 초과
415: 지원하지 않는 이미지 형식
500: 서버 오류

### 실패 응답
```json
{
  "status": 400,
  "message": "사용자 프로필 입력값을 확인해주세요.",
  "data": null
}
```

