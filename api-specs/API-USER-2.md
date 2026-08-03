# [API-USER-2] 회원탈퇴

## 1. 기본 정보

- **Method**: `DELETE`
- **Endpoint**: `/api/users/me`
- **통신 방식**: REST
- **인증 필요**: Y
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Authorization": "Bearer {accessToken}",
  "Content-Type": "application/json"
}

### Request Body
```json
{
  "reason": "string(optional)"
}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "회원탈퇴 성공",
  "data": null
}
```

### Error Codes
401: 인증 필요/토큰 만료
404: 사용자 없음
500: 서버 오류

### 실패 응답
```json
{
  "status": 401,
  "message": "인증이 필요합니다.",
  "data": null
}
```

