# [API-BOOKING-1] 예약 제휴 링크 조회

## 1. 기본 정보

- **Method**: `GET`
- **Endpoint**: `/api/courses/{courseId}/booking-links`
- **통신 방식**: REST
- **인증 필요**: Y
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Authorization": "Bearer {accessToken}"
}

### Path Params
{
  "courseId": "string(UUID)"
}

### Query Params
{
  "type": "hotel | flight"
}

### Request Body
```json
{}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "예약 제휴 링크 조회 성공",
  "data": {
    "bookingLink": {
      "bookingLinkId": "string(UUID)",
      "provider": "agoda",
      "title": "string",
      "url": "string"
    }
  }
}
```

### Error Codes
400: 유효하지 않은 예약 링크 타입
401: 인증 실패
403: 접근 권한 없음
404: 코스 또는 예약 제휴 링크 없음
500: 예약 제휴 링크 조회 실패

### 실패 응답
```json
{
  "status": 400,
  "message": "예약 제휴 링크 타입을 확인해주세요.",
  "data": null
}
```

