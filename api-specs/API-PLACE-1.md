# [API-PLACE-1] 여행 장소 조회

## 1. 기본 정보

- **Method**: `GET`
- **Endpoint**: `/api/places/{placeId}`
- **통신 방식**: REST
- **인증 필요**: Y
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Authorization": "Bearer {accessToken}"
}

### Path Params
placeId: Google Place ID 또는 내부 장소 ID

### Request Body
```json
{}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "장소 상세 조회 성공",
  "data": {
    "place": {
      "placeId": "string",
      "placeName": "string",
      "category": "string",
      "address": "string",
      "latitude": "number",
      "longitude": "number",
      "rating": "number|null",
      "photoUrls": ["string"],
      "openingHours": ["string"]
    }
  }
}
```

### Error Codes
400: 잘못된 placeId
401: 인증 실패
404: 장소 없음
500: 서버/외부 API 오류

### 실패 응답
```json
{
  "status": 404,
  "message": "장소 정보를 찾을 수 없습니다.",
  "data": null
}
```

