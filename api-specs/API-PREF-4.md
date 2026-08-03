# [API-PREF-4] 취향 조회

## 1. 기본 정보

- **Method**: `GET`
- **Endpoint**: `/api/users/me/taste-profile`
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
  "message": "성향 프로필 조회 성공",
  "data": {
    "tasteProfile": {
      "tasteProfileId": "string(UUID)",
      "userId": "string(UUID)",
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
      "seasonalEnvironmentPreference": ["warm_region | cold_region | summer_resort | winter_sports | spring_flower_autumn_foliage | dry_weather | off_season | peak_season"]
    }
  }
}
```

### Error Codes
401: 인증 필요/토큰 만료
404: 성향 프로필 없음
500: 서버 오류

### 실패 응답
```json
{
  "status": 404,
  "message": "저장된 성향 프로필이 없습니다.",
  "data": null
}
```

## 4. 상세 내용 및 예외 케이스

```json
{
  "tasteId": "string",
  "userId": "string",
  "updatedAt": "string(YYYY-MM-DD)",
  "travelPurpose": {
    "relaxation": "int",
    "sightseeing": "int",
    "culturalExperience": "int",
    "gourmet": "int",
    "natureExploration": "int",
    "activity": "int",
    "shopping": "int",
    "festivalEvent": "int",
    "wellness": "int",
    "selfDevelopment": "int"
  },
  "travelPaceDensity": "string",
  "preferredLocationType": {
    "bigCity": "int",
    "smallTownAlley": "int",
    "natureHinterland": "int",
    "beachResort": "int",
    "mountainPlateau": "int",
    "historicalCity": "int",
    "themeParkResort": "int",
    "famousSpotPreferred": "int",
    "hiddenSpotPreferred": "int"
  },
  "activityPreference": {
    "viewing": "int",
    "experience": "int",
    "adventure": "int",
    "photographyVideo": "int",
    "gourmetExploration": "int",
    "nightlife": "int",
    "shopping": "int",
    "relaxation": "int",
    "localInteraction": "int"
  },
  "spendingTendency": "string",
  "companionType": "string",
  "foodPreference": {
    "localFoodActive": "int",
    "famousRestaurantCentered": "int",
    "streetFood": "int",
    "cafeDessert": "int",
    "fineDining": "int",
    "familiarFoodPreferred": "int",
    "dietaryRestriction": "int",
    "sightseeingOverFood": "int"
  },
  "seasonalEnvironmentPreference": [
    "string"
  ]
}
```
