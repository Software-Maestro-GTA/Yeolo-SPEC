# [API-COURSE-3] 여행 코스 목록 조회

## 1. 기본 정보

- **Method**: `GET`
- **Endpoint**: `/api/courses`
- **통신 방식**: REST
- **인증 필요**: Y
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Authorization": "Bearer {accessToken}"
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
  "message": "여행 코스 목록 조회 성공",
  "data": {
    "courses": [
      {
        "courseId": "string(UUID)",
        "title": "string",
        "destinationCountry": "string",
        "destinationCity": "string",
        "coverImageUrl": "string",
        "startDate": "string(YYYY-MM-DD)",
        "totalDays": "number",
        "tags": ["string"],
        "recommendationReason": "string",
        "createdAt": "string(ISO-8601)"
      }
    ]
  }
}
```

### Error Codes
401: 인증 실패
500: 서버 오류

### 실패 응답
```json
{
  "status": 500,
  "message": "여행 코스 목록 조회 실패",
  "data": null
}
```

