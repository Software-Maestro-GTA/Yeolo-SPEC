# [API-FB-7] 여행 코스 상세 조회

기존에 빌드 완료되어 저장된 특정 여행 코스 고유 ID를 조회하여, 해당 코스의 모든 세부 일정 목록(Stop-by-Stop 여정 구조 및 이동 상세)과 맵 정보를 반환합니다.

---

## 1. API 개요

- **Endpoint**: `/api/courses/{courseId}`
- **Method**: `GET`
- **통신 방식**: `REST`
- **인증 필요**: `true`
- **Header**:
  ```json
  {
    "Authorization": "Bearer {accessToken}"
  }
  ```

---

## 2. Request 사양

### Path Parameters

```json
{
  "courseId": "string(UUID)"
}
```

---

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
      "totalCost": "number",
      "tags": ["string"],
      "recommendationReason": "string",
      "constraints": {
        "budgetType": "cost_effective | standard | luxury",
        "maxTravelMinutesPerDay": "number",
        "preferredTransport": ["walking | transit | driving | taxi"],
        "pace": "relaxed | balanced | dense"
      },
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

---

## 4. 에러 코드 및 예외 처리

- **401**: 인증 필요/토큰 만료
- **403**: 접근 권한 없음
- **404**: 코스 없음
- **500**: 서버 오류

### 실패 응답 (Status 404)

```json
{
  "status": 404,
  "message": "여행 코스를 찾을 수 없습니다.",
  "data": null
}
```
