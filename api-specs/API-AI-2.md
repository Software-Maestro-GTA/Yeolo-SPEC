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
"Content-Type": "application/json",
"Accept-Language": "ko"
}

### Path Params

{}

### Query Params

{}

### Request Body

```json
{
  "userId": "string(UUID)",
  "language": "string",
  "mbti": "string|null",
  "tasteProfile": "object|null",
  "tripCondition": {
    "destinationCountry": "string",
    "destinationCity": "string",
    "startDate": "string(YYYY-MM-DD)",
    "totalDays": "number",
    "budget": "number"
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
    "startDate": "string(YYYY-MM-DD)",
    "totalDays": "number",
    "totalCost": "number",
    "tags": ["string"],
    "itinerary": {
      "days": [
        {
          "day": "number",
          "date": "string(YYYY-MM-DD)",
          "stops": [
            {
              "sequence": "number",
              "stayMinutes": "number",
              "memo": "string",
              "reason": "string",
              "cost": "number",
              "place": {
                "placeId": "string",
                "placeName": "string",
                "category": "string",
                "latitude": "number",
                "longitude": "number"
               },
              "transportToNext": {
                "type": "walking | transit | driving | taxi | none",
                "distance": "number|null",
                "minutes": "number|null",
                "memo": "string|null"
              }
            }
          ]
        }
      ]
    }
  }
};
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

## 4. 상세 내용 및 예외 케이스

## 사진 출처 전용 응답 필드 (2026-10-02)

사용자 승인에 따라 완료 응답에 사진 출처 전용 필드 두 개를 추가합니다. `reason`은 장소 추천의 근거, 장소 `memo`는 방문 팁, `transportToNext.memo`는 이동 안내로 사용합니다. 사진 출처를 이 본문에 합치지 않습니다.

### 추가한 필드

| 경로                                                     | 타입·기본값       | 사용 방식        |
| :------------------------------------------------------- | :---------------- | :--------------- | -------------------------------------------------------------- |
| `course.coverImageAttribution`                           | `PhotoAttribution | null`, 기본 null | 대표 이미지로 선택한 장소 사진과 같은 출처입니다.              |
| `course.itinerary.days[].stops[].place.photoAttribution` | `PhotoAttribution | null`, 기본 null | 해당 `photoUrl`의 원본 링크와 제공된 작성자 정보를 전달합니다. |

### PhotoAttribution

`provider`는 `"Google Maps"`, `googleMapsUri`는 개별 원본 사진 링크입니다. `authorAttributions`는 제공된 모든 작성자 목록이며 기본값은 빈 배열입니다. 각 작성자의 `displayName`은 필수이고 `uri`(프로필)와 `photoUri`(작성자 프로필 이미지)는 제공된 경우만 값이 있으며 그 외에는 null입니다. 작성자 프로필 이미지를 장소 사진으로 사용하지 않습니다.

```json
{
  "provider": "Google Maps",
  "googleMapsUri": "https://www.google.com/maps/...",
  "authorAttributions": [
    {
      "displayName": "제공된 작성자 이름",
      "uri": "https://www.google.com/maps/contrib/...",
      "photoUri": "https://lh3.googleusercontent.com/..."
    }
  ]
}
```

사진을 확보하지 못하면 이미지 URL은 기존처럼 빈 문자열이고 출처는 null입니다. 요청 본문, 엔드포인트, progress·complete 이벤트 이름과 progress의 step 계약은 그대로입니다. 이전 완료 응답에서 이 필드가 생략된 경우도 기본 null로 읽습니다.

### BE·FE 연결 사항

AI 서버가 필드를 추가했다고 기존 BE 저장·전달 DTO나 FE 표시가 자동으로 바뀌지는 않습니다. BE는 두 필드와 작성자 목록을 보존하여 FE에 전달하고, FE는 팁과 분리한 이미지 영역에서 Google Maps와 작성자·원본 링크를 표시해야 합니다. 알 수 없는 필드를 거부하는 DTO가 있으면 함께 갱신해야 합니다. 이 AI 저장소에는 실제 BE·FE 표시 구현을 포함하지 않습니다.

썸네일에서 작성자 표시를 생략하는 경우에는 전체 작성자 표시가 있는 확대 이미지로 연결하고 개별 원본 사진에 접근할 수 있어야 합니다. [Google Places 사진 표시 정책](https://developers.google.com/maps/documentation/places/web-service/policies#photos_and_reviews)

현재 구현·검증·PR 상태는 [코스 생성 프로세스](https://app.notion.com/p/3ad1d7341cda8031a02bce2ea8b00c4c)에 기록합니다.
