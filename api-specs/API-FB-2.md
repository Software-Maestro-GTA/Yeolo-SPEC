# [API-FB-2] 이미지 메타데이터 기반 성향 분석 생성

클라이언트 측에서 제공받은 여행 사진 메타데이터 목록을 받아, 백엔드 전처리 및 AI 분석 엔진과의 연동을 거쳐 성향 프로필이 완성되기까지의 진행 상황을 실시간 스트리밍으로 전달합니다.

---

## 1. API 개요

- **Endpoint**: `/api/taste-profile/behavior`
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
  "images": [
    {
      "sourceImageId": "string",
      "capturedAt": "string(ISO-8601)",
      "latitude": "number",
      "longitude": "number",
      "timezone": "string"
    }
  ]
}
```

---

## 3. Response 사양

### 성공 응답 (SSE Stream)

```text
event: progress
data: {"step":"PREPROCESSING_IMAGE_METADATA","message":"이미지 위치·시간 정보를 전처리 중입니다."}

event: progress
data: {"step":"ANALYZING_PREFERENCE","message":"여행 성향을 분석 중입니다."}

event: complete
data: {"status":200,"message":"행동 데이터 기반 성향 분석 생성 성공","data":{"tasteProfileId":"string(UUID)","sourceType":"behavior"}}
```

---

## 4. 에러 코드 및 예외 처리

- **400**: 이미지 메타데이터 부족/형식 오류
- **401**: 인증 필요/토큰 만료
- **403**: 개인정보 수집·활용 동의 없음
- **500**: 서버 또는 AI 분석 오류

### 실패 응답 (Status 400)

```json
{
  "status": 400,
  "message": "분석 가능한 이미지 메타데이터가 부족합니다.",
  "data": null
}
```
