# [API-BA-1] [BE-AI] 성향 프로필 기반 여행 코스 생성

백엔드 서버(BE)와 AI 서버(AI) 간의 내부 통신 인터페이스 규격입니다. 백엔드에서 정규화하여 전달한 성향 프로필과 여행의 제약 조건들을 해석해, AI 엔진이 최적의 일자별 스톱(Stop) 여정과 추천 이유(Itinerary)를 빌드하여 스트리밍 전달합니다.

---

## 1. API 개요

- **Endpoint**: `/internal/ai/courses`
- **Method**: `POST`
- **통신 방식**: `SSE`
- **인증 필요**: `true`
- **Header**:
  ```json
  {
    "X-Internal-Api-Key": "{internalApiKey}"
  }
  ```

---

## 2. Request 사양

### Body

```json
{
  "userId": "string(UUID)",
  "tasteProfile": {
    "tasteProfileId": "string(UUID)",
    "sourceType": "survey | behavior | mixed",
    "travelPurpose": {
      "relaxation": "number(1-5)",
      "sightseeing": "number(1-5)",
      "gourmet": "number(1-5)",
      "natureExploration": "number(1-5)"
    },
    "travelPaceDensity": "slow_stay | balanced | dense_schedule | spontaneous | long_stay",
    "preferredLocationType": {
      "bigCity": "number(1-5)",
      "smallTownAlley": "number(1-5)",
      "natureHinterland": "number(1-5)",
      "beachResort": "number(1-5)",
      "hiddenSpotPreferred": "number(1-5)"
    },
    "activityPreference": {
      "viewing": "number(1-5)",
      "experience": "number(1-5)",
      "photographyVideo": "number(1-5)",
      "gourmetExploration": "number(1-5)",
      "relaxation": "number(1-5)"
    },
    "spendingTendency": "cost_effective | moderate | luxury",
    "companionType": "solo | couple | friends | family | with_children | with_parents | group | with_pet | social",
    "foodPreference": {
      "localFoodActive": "number(1-5)",
      "famousRestaurantCentered": "number(1-5)",
      "streetFood": "number(1-5)",
      "cafeDessert": "number(1-5)"
    },
    "seasonalEnvironmentPreference": ["string"]
  },
  "tripCondition": {
    "destinationCountry": "string",
    "destinationCity": "string",
    "startDate": "string(YYYY-MM-DD)",
    "totalDays": "number",
    "budgetType": "cost_effective | standard | luxury"
  }
}
```

---

## 3. Response 사양

### 성공 응답 (SSE Stream)

```text
event: progress
data: {"step":"GENERATING_ROUTE","message":"장소와 이동 순서를 구성 중입니다."}

event: complete
data: {"course":{"title":"string","destinationCountry":"string","destinationCity":"string","region":"string","startDate":"string(YYYY-MM-DD)","totalDays":"number","totalCost":"number","tags":["string"],"recommendationReason":"string","itinerary":{"days":[{"day":"number","date":"string(YYYY-MM-DD)","memo":"string","stops":[{"sequence":"number","placeId":"string","placeName":"string","category":"string","arrivalTime":"string(HH:mm)","stayMinutes":"number","memo":"string","transportToNext":"walking | transit | driving | taxi | none","travelMinutesToNext":"number","cost":"number","reason":"string"}]}]}}}
```

---

## 4. 에러 코드 및 예외 처리

- **400**: 성향 프로필/여행 조건 누락 또는 형식 오류
- **401**: 내부 인증 실패
- **404**: 조건에 맞는 장소 없음
- **500**: AI 서버 오류

### 실패 응답 (Status 400)

```json
{
  "status": 400,
  "message": "코스 생성 조건이 올바르지 않습니다."
}
```
