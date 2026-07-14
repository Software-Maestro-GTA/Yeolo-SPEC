# [API-BA-6] [BE-AI] 전처리 이미지 메타데이터 기반 성향 분석

백엔드 서버(BE)와 AI 서버(AI) 간의 내부 통신 인터페이스 규격입니다. 백엔드에서 Reverse Geocode 및 시간 데이터 파싱을 끝낸 전처리 사진 메타데이터 목록을 받아, AI 엔진이 사용자의 여행 요일·시간대·계절 및 자주 방문하는 장소의 결합 패턴을 LLM으로 추론하여 정규화된 성향 선호 지표 데이터셋을 리턴합니다.

---

## 1. API 개요

- **Endpoint**: `/internal/ai/taste-profile/behavior`
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
  "items": [
    {
      "sourceImageId": "string",
      "location": {
        "country": "string",
        "city": "string",
        "region": "string",
        "district": "string",
        "placeName": "string",
        "placeTypes": ["string"]
      },
      "timeContext": {
        "capturedAt": "string(ISO-8601)",
        "dayOfWeek": "mon | tue | wed | thu | fri | sat | sun",
        "isWeekend": "boolean",
        "timeBucket": "dawn | morning | afternoon | evening | night",
        "season": "spring | summer | autumn | winter"
      }
    }
  ]
}
```

---

## 3. Response 사양

### 성공 응답 (SSE Stream)

```text
event: progress
data: {"step":"ANALYZING_PREFERENCE","message":"위치·시간 패턴으로 여행 성향을 분석 중입니다."}

event: complete
data: {"tasteProfile":{"sourceType":"behavior","travelPurpose":{"relaxation":"number(1-5)","sightseeing":"number(1-5)","culturalExperience":"number(1-5)","gourmet":"number(1-5)","natureExploration":"number(1-5)","activity":"number(1-5)","shopping":"number(1-5)","festivalEvent":"number(1-5)","wellness":"number(1-5)","selfDevelopment":"number(1-5)"},"travelPaceDensity":"slow_stay | balanced | dense_schedule | spontaneous | long_stay","preferredLocationType":{"bigCity":"number(1-5)","smallTownAlley":"number(1-5)","natureHinterland":"number(1-5)","beachResort":"number(1-5)","mountainPlateau":"number(1-5)","historicalCity":"number(1-5)","themeParkResort":"number(1-5)","famousSpotPreferred":"number(1-5)","hiddenSpotPreferred":"number(1-5)"},"activityPreference":{"viewing":"number(1-5)","experience":"number(1-5)","adventure":"number(1-5)","photographyVideo":"number(1-5)","gourmetExploration":"number(1-5)","nightlife":"number(1-5)","shopping":"number(1-5)","relaxation":"number(1-5)","localInteraction":"number(1-5)"},"spendingTendency":"cost_effective | moderate | luxury","companionType":"solo | couple | friends | family | with_children | with_parents | group | with_pet | social","foodPreference":{"localFoodActive":"number(1-5)","famousRestaurantCentered":"number(1-5)","streetFood":"number(1-5)","cafeDessert":"number(1-5)","fineDining":"number(1-5)","familiarFoodPreferred":"number(1-5)","dietaryRestriction":"number(1-5)","sightseeingOverFood":"number(1-5)"},"seasonalEnvironmentPreference":["warm_region | cold_region | summer_resort | winter_sports | spring_flower_autumn_foliage | dry_weather | off_season | peak_season"]}}
```

---

## 4. 에러 코드 및 예외 처리

- **400**: 전처리 메타데이터 부족/형식 오류
- **401**: 내부 인증 실패
- **500**: AI 서버 오류

### 실패 응답 (Status 400)

```json
{
  "status": 400,
  "message": "분석 가능한 전처리 메타데이터가 부족합니다."
}
```
