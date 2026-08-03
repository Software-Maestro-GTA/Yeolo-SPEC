# [API-SHARE-3] 여행 코스 공유 링크 수락

## 1. 기본 정보

- **Method**: `POST`
- **Endpoint**: `/api/share-links/{shareToken}/accept`
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
  "shareToken": "string"
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
  "message": "여행 코스 공유 수락 성공",
  "data": {
    "courseId": "string(UUID)"
  }
}
```

### Error Codes
400: 이미 수락한 링크/자기 자신의 코스
401: 인증 실패
404: 유효하지 않은 공유 링크/코스 없음
410: 만료되었거나 회수된 공유 링크
500: 공유 수락 실패

### 실패 응답
```json
{
  "status": 400,
  "message": "수락할 수 없는 공유 링크입니다.",
  "data": null
}
```

