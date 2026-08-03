# [API-PREF-2] 사진 데이터 분석 동의 저장

## 1. 기본 정보

- **Method**: `POST`
- **Endpoint**: `/api/users/me/consents/photo`
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
  "agreed": "boolean",
  "consentVersion": "string"
}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "사진 데이터 분석 동의 저장 성공",
  "data": {
    "consent": {
      "agreed": "boolean",
      "agreedAt": "string(ISO-8601)",
      "consentVersion": "string"
    }
  }
}
```

### Error Codes
400: 잘못된 동의 입력값
401: 인증 실패
500: 동의 저장 실패

### 실패 응답
```json
{
  "status": 400,
  "message": "사진 데이터 분석 동의 입력값을 확인해주세요.",
  "data": null
}
```

