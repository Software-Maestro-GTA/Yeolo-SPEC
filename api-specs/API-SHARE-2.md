# [API-SHARE-2] 여행 코스 공유 링크 조회

## 1. 기본 정보

- **Method**: `GET`
- **Endpoint**: `/api/share-links/{shareToken}`
- **통신 방식**: REST
- **인증 필요**: N
- **Success Status**: `200`

## 2. Request 사양

### Header
{}

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
  "message": "여행 코스 공유 링크 조회 성공",
  "data": {
    "course": {
      "title": "string",
      "destinationCountry": "string",
      "destinationCity": "string",
      "startDate": "string(YYYY-MM-DD)",
      "totalDays": "number"
    },
    "inviter": {
      "displayName": "string|null",
      "profileImageUrl": "string|null"
    },
    "expiresAt": "string(ISO-8601)|null"
  }
}
```

### Error Codes
404: 유효하지 않은 공유 링크/코스 없음
410: 만료되었거나 회수된 공유 링크
500: 공유 링크 조회 실패

### 실패 응답
```json
{
  "status": 404,
  "message": "유효하지 않은 공유 링크입니다.",
  "data": null
}
```

