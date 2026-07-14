# [API-FB-3] 최소 설문 기반 성향 분석 생성

사용자가 입력한 최소 설문 응답(1~5점 척도 선호 점수 및 유형 단일/다중 선택지)을 기반으로 정규화된 여행 성향 프로필(Taste Profile)을 생성하고 보관합니다.

---

## 1. API 개요

- **Endpoint**: `/api/taste-profile/survey`
- **Method**: `POST`
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

### Body

```json
{
  "sourceType": "survey",
  "travelPurpose": {
    "relaxation": "number(1-5)",
    "sightseeing": "number(1-5)",
    "culturalExperience": "number(1-5)",
    "gourmet": "number(1-5)",
    "natureExploration": "number(1-5)",
    "activity": "number(1-5)",
    "shopping": "number(1-5)",
    "festivalEvent": "number(1-5)",
    "wellness": "number(1-5)",
    "selfDevelopment": "number(1-5)"
  },
  "travelPaceDensity": "slow_stay | balanced | dense_schedule | spontaneous | long_stay",
  "preferredLocationType": {
    "bigCity": "number(1-5)",
    "smallTownAlley": "number(1-5)",
    "natureHinterland": "number(1-5)",
    "beachResort": "number(1-5)",
    "mountainPlateau": "number(1-5)",
    "historicalCity": "number(1-5)",
    "themeParkResort": "number(1-5)",
    "famousSpotPreferred": "number(1-5)",
    "hiddenSpotPreferred": "number(1-5)"
  },
  "activityPreference": {
    "viewing": "number(1-5)",
    "experience": "number(1-5)",
    "adventure": "number(1-5)",
    "photographyVideo": "number(1-5)",
    "gourmetExploration": "number(1-5)",
    "nightlife": "number(1-5)",
    "shopping": "number(1-5)",
    "relaxation": "number(1-5)",
    "localInteraction": "number(1-5)"
  },
  "spendingTendency": "cost_effective | moderate | luxury",
  "companionType": "solo | couple | friends | family | with_children | with_parents | group | with_pet | social",
  "foodPreference": {
    "localFoodActive": "number(1-5)",
    "famousRestaurantCentered": "number(1-5)",
    "streetFood": "number(1-5)",
    "cafeDessert": "number(1-5)",
    "fineDining": "number(1-5)",
    "familiarFoodPreferred": "number(1-5)",
    "dietaryRestriction": "number(1-5)",
    "sightseeingOverFood": "number(1-5)"
  },
  "seasonalEnvironmentPreference": [
    "warm_region | cold_region | summer_resort | winter_sports | spring_flower_autumn_foliage | dry_weather | off_season | peak_season"
  ]
}
```

---

## 3. Response 사양

### 성공 응답 (Status 200)

```json
{
  "status": 200,
  "message": "설문 기반 성향 프로필 저장 성공",
  "data": {
    "tasteProfileId": "string(UUID)",
    "sourceType": "survey"
  }
}
```

---

## 4. 에러 코드 및 예외 처리

- **400**: 필수 설문 응답 누락/점수 범위 오류
- **401**: 인증 필요/토큰 만료
- **500**: 서버 오류

### 실패 응답 (Status 400)

```json
{
  "status": 400,
  "message": "필수 설문 응답이 누락되었습니다.",
  "data": null
}
```
