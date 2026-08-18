# [API-AI-2] 여행 코스 생성

## 1. 기본 정보

- **Method**: `POST`
- **Endpoint**: `/internal/ai/courses`
- **통신 방식**: SSE
- **인증 필요**: Y
- **Success Status**: `200`

## 2. Request 사양

### Header

{
"X-Internal-Api-Key": "{internalApiKey}",
"Content-Type": "application/json"
}

### Path Params

{}

### Query Params

{}

### Request Body

```json
{
  "userId": "string(UUID)",
  "mbti": "string|null",
  "tasteProfile": "object|null",
  "tripCondition": {
    "destinationCountry": "string",
    "destinationCity": "string",
    "startDate": "string(YYYY-MM-DD)",
    "totalDays": "number",
    "budgetType": "cost_effective | moderate | luxury"
  }
}
```

## 3. Response 사양

### 성공 응답 (Status 200)

```json
event: progress
data: {
  "step": "GENERATING_ROUTE",
  "message": "장소와 이동 순서를 구성 중입니다."
}

event: complete
data: {
  "course": {
    "title": "string",
    "destinationCountry": "string",
    "destinationCity": "string",
    "coverImageUrl": "string",
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
              "arrivalTime": "string(HH:mm)",
              "stayMinutes": "number",
              "memo": "string",
              "reason": "string",
              "cost": "number",
              "place": {
                "placeId": "string",
                "placeName": "string",
                "placeEngName": "string",
                "category": "string",
                "address": "string",
                "latitude": "number",
                "longitude": "number",
                "rating": "number|null",
                "photoUrl": "string",
                "openingHours": ["string"]
              },
              "transportToNext": {
                "type": "walking | transit | driving | taxi | none",
                "distance": "number|null",
                "minutes": "number|null",
                "cost": "number|null",
                "memo": "string|null"
              }
            }
          ]
        }
      ]
    }
  }
}
```

### Error Codes

400: 성향 프로필/여행 조건 누락 또는 형식 오류
401: 내부 인증 실패
404: 조건에 맞는 장소 없음
500: AI 서버 오류

### 실패 응답

```json
{
  "status": 400,
  "message": "코스 생성 조건이 올바르지 않습니다.",
  "data": null
}
```
