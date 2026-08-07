# [API-COURSE-1] 여행 코스 생성

## 1. 기본 정보

- **Method**: `POST`
- **Endpoint**: `/api/courses`
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
  "destinationCountry": "string",
  "destinationCity": "string",
  "startDate": "string(YYYY-MM-DD)",
  "totalDays": "number",
  "budgetType": "cost_effective | moderate | luxury"
}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
event: progress
data: {
  "step": "LOADING_TASTE_PREFERENCE",
  "message": "사용자 정보를 불러오는 중입니다."
}

event: progress
data: {
  "step": "GENERATING_COURSE",
  "message": "개인 맞춤형 여행 코스를 생성 중입니다."
}

event: complete
data: {
  "status": 200,
  "message": "여행 코스 생성 성공",
  "data": {
    "courseId": "string(UUID)"
  }
}
```

### Error Codes
400: 필수 여행 조건 누락/잘못된 국가·도시
401: 인증 실패
404: 성향 정보 없음
500: 코스 생성 실패

### 실패 응답
```json
{
  "status": 400,
  "message": "국가, 도시, 일정, 예산 등 필수 여행 조건을 확인해주세요.",
  "data": null
}
```

