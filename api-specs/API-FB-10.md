# [API-FB-10] 이전 생성 코스 목록 조회

해당 사용자가 생성했거나 보유하고 있는 이전 여행 추천 코스 데이터들의 간략한 메타데이터 목록을 페이지네이션 및 최신 순으로 정렬하여 조회합니다.

---

## 1. API 개요

- **Endpoint**: `/api/courses`
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

- 별도의 Query Parameter 또는 Request Body 없음.

---

## 3. Response 사양

### 성공 응답 (Status 200)

```json
{
  "status": 200,
  "message": "이전 생성 코스 목록 조회 성공",
  "data": {
    "courses": [
      {
        "courseId": "string(UUID)",
        "title": "string",
        "destinationCountry": "string",
        "destinationCity": "string",
        "region": "string",
        "startDate": "string(YYYY-MM-DD)",
        "totalDays": "number",
        "totalCost": "number",
        "tags": ["string"],
        "recommendationReason": "string",
        "createdAt": "string(ISO-8601)"
      }
    ]
  }
}
```

---

## 4. 에러 코드 및 예외 처리

- **401**: 인증 필요/토큰 만료
- **500**: 서버 오류

### 실패 응답 (Status 401)

```json
{
  "status": 401,
  "message": "인증이 필요합니다.",
  "data": null
}
```
