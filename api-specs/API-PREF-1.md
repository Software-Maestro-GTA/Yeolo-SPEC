# [API-PREF-1] 사용자 MBTI 등록/수정

## 1. 기본 정보

- **Method**: `PATCH`
- **Endpoint**: `/api/users/me/preferences`
- **통신 방식**: REST
- **인증 필요**: Y
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Authorization": "Bearer {accessToken}",
  "Content-Type": "application/json"
}

### Path Params
{}

### Query Params
{}

### Request Body
```json
{
  "mbti": "string"
}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "사용자 MBTI 수정 성공",
  "data": null
}
```

### Error Codes
400: 잘못된 MBTI 입력값
401: 인증 실패
500: 서버 오류

### 실패 응답
```json
{
  "status": 400,
  "message": "MBTI 입력값을 확인해주세요.",
  "data": null
}
```

