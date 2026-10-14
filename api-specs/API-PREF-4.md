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
  "Authorization": "Bearer {accessToken}",
  "Accept-Language": "ko"
}

### Request Body
```json
{}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": "number",
  "message": "string",
  "data": {
    "intro": "string",
    "hashtags": [
      "string"
    ],
    "types": [
      {
        "typeCode": "string",
        "typeName": "string",
        "lowName": "string",
        "highName": "string",
        "score": "number"
      }
    ],
    "recommendCity": {
      "countryName": "string",
      "cityName": "string",
      "imageUrl": "string",
      "reason": "string"
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
