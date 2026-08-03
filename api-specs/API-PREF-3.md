# [API-PREF-3] 취향 분석

## 1. 기본 정보

- **Method**: `POST`
- **Endpoint**: `/api/users/me/taste-profile/analysis`
- **통신 방식**: SSE
- **인증 필요**: Y
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Authorization": "Bearer {accessToken}",
  "Content-Type": "application/json"
}

### Request Body
```json
{
  "images": [
    {
      "sourceImageId": "string",
      "capturedAt": "string(ISO-8601 UTC)",
      "latitude": "number",
      "longitude": "number"
    }
  ]
}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
event: progress
data: {
  "step": "PREPROCESSING_IMAGE_METADATA",
  "message": "이미지 위치·시간 정보를 전처리 중입니다."
}

event: progress
data: {
  "step": "ANALYZING_PREFERENCE",
  "message": "여행 취향을 분석 중입니다."
}

event: complete
data: {
  "status": 200,
  "message": "행동 데이터 기반 취향 분석 생성 성공",
  "data": {
    "tasteProfileId": "string(UUID)"
  }
}
```

### Error Codes
400: 이미지 메타데이터 부족/형식 오류
401: 인증 필요/토큰 만료
403: 개인정보 수집·활용 동의 없음
500: 서버 또는 AI 분석 오류

### 실패 응답
```json
{
  "status": 400,
  "message": "분석 가능한 이미지 메타데이터가 부족합니다.",
  "data": null
}
```

