# [API-COURSE-4] 여행 코스 삭제

## 1. 기본 정보

- **Method**: `DELETE`
- **Endpoint**: `/api/courses/{courseId}`
- **통신 방식**: REST
- **인증 필요**: Y
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Authorization": "Bearer {accessToken}"
}

### Path Params
courseId: 삭제할 여행 코스 ID

### Request Body
```json
{}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "여행 코스 삭제 성공",
  "data": null
}
```

### Error Codes
401: 인증 실패
403: 권한 없음
404: 코스 없음
500: 서버 오류

### 실패 응답
```json
{
  "status": 403,
  "message": "해당 여행 코스를 삭제할 권한이 없습니다.",
  "data": null
}
```

