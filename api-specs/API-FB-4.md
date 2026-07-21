# [API-FB-4] 개인 맞춤형 여행 코스 생성

사용자가 신규 입력한 여행지 정보(지역/날짜/예산)에 기반해 사용자의 성향 프로필을 로딩한 후 AI 엔진으로 코스를 생성하는 과정을 실시간으로 스트리밍 처리합니다.

---

## 1. API 개요

- **Endpoint**: `/api/courses`
- **Method**: `POST`
- **통신 방식**: `SSE`
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
  "destinationCountry": "string",
  "destinationCity": "string",
  "startDate": "string(YYYY-MM-DD)",
  "totalDays": "number",
  "budgetType": "cost_effective | standard | luxury"
}
```

---

## 3. Response 사양

### 성공 응답 (SSE Stream)

```text
event: progress
data: {"step":"LOADING_TASTE_PROFILE","message":"사용자 성향 프로필을 불러오는 중입니다."}

event: progress
data: {"step":"GENERATING_COURSE","message":"개인 맞춤형 여행 코스를 생성 중입니다."}

event: complete
data: {"status":200,"message":"여행 코스 생성 성공","data":{"courseId":"string(UUID)"}}
```

---

## 4. 에러 코드 및 예외 처리

- **400**: 필수 여행 조건 누락/형식 오류
- **401**: 인증 필요/토큰 만료
- **404**: 성향 프로필 없음
- **500**: 서버 또는 AI 코스 생성 오류

### 실패 응답 (Status 400)

```json
{
  "status": 400,
  "message": "여행 조건 입력값이 올바르지 않습니다.",
  "data": null
}
```
