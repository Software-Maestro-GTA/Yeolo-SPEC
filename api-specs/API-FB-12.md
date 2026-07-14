# [API-FB-12] 회원탈퇴

사용자의 계정을 비활성/삭제 처리하고, 저장된 개인정보 및 연동된 행동 데이터 등을 영구히 파기합니다.

---

## 1. API 개요

- **Endpoint**: `/api/users/me`
- **Method**: `DELETE`
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

### Body

```json
{
  "reason": "string(optional)"
}
```

---

## 3. Response 사양

### 성공 응답 (Status 200)

```json
{
  "status": 200,
  "message": "회원탈퇴 성공",
  "data": null
}
```

---

## 4. 에러 코드 및 예외 처리

- **401**: 인증 필요/토큰 만료
- **404**: 사용자 없음
- **500**: 서버 오류

### 실패 응답 (Status 401)

```json
{
  "status": 401,
  "message": "인증이 필요합니다.",
  "data": null
}
```
