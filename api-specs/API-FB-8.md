# [API-FB-8] 내 성향 프로필 조회

사용자가 이전에 완료하여 저장해 둔 정규화된 여행 성향 프로필(Taste Profile) 상세 정보를 조회합니다.

---

## 1. API 개요

- **Endpoint**: `/api/me/taste-profile`
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

- **Query Params**: 없음
- **Path Params**: 없음
- **Request Body**: 없음

---

## 3. Response 사양

### 성공 응답 (Status 200)

```json
{
  "status": 200,
  "message": "성향 프로필 조회 성공",
  "data": {
    "tasteProfile": {
      "tasteProfileId": "string(UUID)",
      "userId": "string(UUID)",
      "sourceType": "survey | behavior | mixed",
      "updatedAt": "string(YYYY-MM-DD)",
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
  }
}
```

---

## 4. 에러 코드 및 예외 처리

- **401**: 인증 필요/토큰 만료
- **404**: 성향 프로필 없음
- **500**: 서버 오류

### 실패 응답 (Status 404)

```json
{
  "status": 404,
  "message": "저장된 성향 프로필이 없습니다.",
  "data": null
}
```
