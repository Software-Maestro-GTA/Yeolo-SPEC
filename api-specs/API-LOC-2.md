# [API-LOC-2] 국가별 도시 전체 목록 조회

## 1. 기본 정보

- **Method**: `GET`
- **Endpoint**: `/api/locations/cities`
- **통신 방식**: REST
- **인증 필요**: N
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Accept-Language": "ko"
}

### Path Params
없음

### Query Params
{
  "countryName": "string"
}

### Request Body
```json
없음
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "도시 목록 조회 성공",
  "data": {
    "cities": [
      {
        "cityName": "string"
      }
    ]
  }
}
```

### Error Codes
400: countryName 누락, 빈 문자열 또는 잘못된 형식
404: 해당 국가 없음
500: 도시 목록 조회 실패/서버 오류

### 실패 응답
```json
{
  "status": 500,
  "message": "도시 목록 조회에 실패했습니다.",
  "data": null
}
```

## 4. 상세 내용 및 예외 케이스

## 기능

국가 ID 또는 국가 이름으로 국가를 지정하면 해당 국가의 서비스 등록 도시 전체 목록을 반환한다. `keyword`, `limit`, 페이지네이션은 사용하지 않는다.


## 요청 규칙

- `countryId` 또는 `country` 중 정확히 하나를 필수로 전달한다. 둘 다 전달하거나 둘 다 누락하면 `400`을 반환한다.
- `countryId`: API-LOC-1에서 받은 국가 식별자. 화면에서 국가 선택 시 ID 사용을 권장한다.
- `country`: 국가 이름. 앞뒤 공백 제거 후 등록된 국가명 또는 다국어 별칭과 완전 일치로 조회한다. 부분·접두어 검색은 API-LOC-3을 사용한다.
- 이름 비교는 영문 대소문자를 구분하지 않는다. 국가 ID는 식별자 그대로 비교한다.
- 존재하지 않는 국가면 `404`, 존재하는 국가에 등록 도시가 없으면 `200`과 `cities: []`를 반환한다.

## 요청 예시

```javascript
GET /api/locations/cities?countryId={countryId}
Accept-Language: ko
```

```javascript
GET /api/locations/cities?country=일본
Accept-Language: ko
```

실제 요청에서는 쿼리 값을 URL 인코딩한다.


## 응답 및 화면 연결

- 선택한 국가의 전체 도시를 표시명 기준 오름차순으로 반환하고 도시 ID 기준 중복을 제거한다.
- `cityId`, `countryId`는 언어와 무관한 식별자이며, `city`, `country`는 응답 언어에 맞는 표시명이다.
- 도시를 선택하면 해당 도시와 국가의 선택을 완료한다.

## 언어 정책

기존 `Accept-Language` 헤더를 유지한다. 지원 언어 중 요청 우선순위에 맞는 언어를 적용하며, 헤더가 없거나 지원 언어가 매칭되지 않으면 서비스 기본 언어를 사용한다. 지원 언어 목록 및 기본값은 별도 확정한다. 국가·도시 표시명과 응답 메시지에 적용하며, ID는 번역하지 않는다.
