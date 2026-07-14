# [API-FB-11] 로그아웃

사용자의 로그인 세션을 종료하고 발급된 리프레시 토큰(Refresh Token)을 무효화합니다.

---

## 1. API 개요

- **Endpoint**: `/api/auth/logout`
- **Method**: `POST`
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
  "refreshToken": "string(optional)"
}
```

---

## 3. Response 사양

### 성공 응답 (Status 200)

```json
{
  "status": 200,
  "message": "로그아웃 성공",
  "data": null
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
