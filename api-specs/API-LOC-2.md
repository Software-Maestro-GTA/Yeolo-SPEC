# [API-LOC-2] 도시 자동완성 조회

## 1. 기본 정보

- **Method**: `GET`
- **Endpoint**: `/api/locations/cities/autocomplete`
- **통신 방식**: REST
- **인증 필요**: N
- **Success Status**: `200`

## 2. Request 사양

### Header
{}

### Path Params
{}

### Query Params
{
  "country": "string(optional)",
  "keyword": "string",
  "limit": "number(optional)"
}

### Request Body
```json
{}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "도시 자동완성 조회 성공",
  "data": {
    "cities": [
      {
        "cityId": "string",
        "cityNameKo": "string",
        "countryId": "string",
        "countryNameKo": "string"
      }
    ]
  }
}
```

### Error Codes
400: 유효하지 않은 검색어
500: 서버 오류

### 실패 응답
```json
{
  "status": 400,
  "message": "도시 검색어를 확인해주세요.",
  "data": null
}
```

