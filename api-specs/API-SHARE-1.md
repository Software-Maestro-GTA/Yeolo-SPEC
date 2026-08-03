# [API-SHARE-1] 여행 코스 공유 링크 생성

## 1. 기본 정보

- **Method**: `POST`
- **Endpoint**: `/api/courses/{courseId}/share-links`
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
{
  "courseId": "string(UUID)"
}

### Query Params
{}

### Request Body
```json
{}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "여행 코스 공유 링크 생성 성공",
  "data": {
    "shareUrl": "string",
    "shareToken": "string",
    "expiresAt": "string(ISO-8601)|null"
  }
}
```

### Error Codes
401: 인증 실패
403: 공유 권한 없음
404: 코스 없음
500: 공유 링크 생성 실패

### 실패 응답
```json
{
  "status": 403,
  "message": "해당 여행 코스를 공유할 권한이 없습니다.",
  "data": null
}
```

