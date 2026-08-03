# [API-COURSE-2] 여행 코스 조회

## 1. 기본 정보

- **Method**: `GET`
- **Endpoint**: `/api/courses/{courseId}`
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

### Request Body
```json
{}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "여행 코스 조회 성공",
  "data": {
    "course": {
      "courseId": "string(UUID)",
      "userId": "string(UUID)",
      "title": "string",
      "destinationCountry": "string",
      "destinationCity": "string",
      "startDate": "string(YYYY-MM-DD)",
      "totalDays": "number",
      "tags": ["string"],
      "recommendationReason": "string",
      "itinerary": {
        "days": [
          {
            "day": "number",
            "date": "string(YYYY-MM-DD)",
            "memo": "string",
            "stops": [
              {
                "sequence": "number",
                "placeId": "string",
                "placeName": "string",
                "category": "string",
                "latitude": "number",
                "longitude": "number",
                "arrivalTime": "string(HH:mm)",
                "stayMinutes": "number",
                "memo": "string",
                "transportToNext": "walking | transit | driving | taxi | none",
                "travelMinutesToNext": "number",
                "cost": "number",
                "reason": "string"
              }
            ]
          }
        ]
      }
    }
  }
}
```

### Error Codes
401: 인증 필요/토큰 만료
403: 접근 권한 없음
404: 코스 없음
500: 서버 오류

### 실패 응답
```json
{
  "status": 404,
  "message": "여행 코스를 찾을 수 없습니다.",
  "data": null
}
```

## 4. 상세 내용 및 예외 케이스

```json
{
  "courseId": "string",
  "title": "string",
  "region": "string",
  "startday": "string(YYYY-MM-DD)",
  "duration": "string",
  "total_cost": "int",
  "days": [
    {
      "day": "int",
      "memo": "string",
      "stops": [
        {
          "sequence": "int",
          "placeName": "string",
          "category": "string",
          "arrival_time": "string(HH:MM)",
          "stay_minutes": "int",
          "memo": "string",
          "transport_to_next": "string",
          "cost": "int",
          "place_id": "string"
        }
      ]
    }
  ]
}
```
