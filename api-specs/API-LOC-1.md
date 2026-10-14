# [API-LOC-1] 국가 전체 목록 조회

## 1. 기본 정보

- **Method**: `GET`
- **Endpoint**: `/api/locations/countries`
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
없음

### Request Body
```json
없음
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "국가 목록 조회 성공",
  "data": {
    "countries": [
      {
        "countryName": "string"
      }
    ]
  }
}
```

### Error Codes
500: 국가 목록 조회 실패/서버 오류

### 실패 응답
```json
{
  "status": 500,
  "message": "국가 목록 조회에 실패했습니다.",
  "data": null
}
```

## 4. 상세 내용 및 예외 케이스

## 기능

입력창의 국가 탐색에 사용할 서비스가 지원하는 국가 전체 목록을 반환한다. 검색 API가 아니므로 `keyword`, `limit`, 페이지네이션을 사용하지 않는다.


## 응답 규칙

- `countries`: 서비스에 등록된 전체 국가 목록. 데이터가 없으면 `200`과 빈 배열을 반환한다.
- `countryId`: 언어가 바뀌어도 동일한 국가 식별자.
- `country`: 응답 언어에 맞는 국가 표시명.
- 표시명 기준 오름차순으로 정렬하고, 국가 ID 기준 중복을 제거한다.

## 화면 연결

- 입력창을 열었을 때 국가 목록을 조회한다.
- 기본 ‘전체’ 화면의 추천 항목과 인기 도시는 클라이언트에서 미리 선정하여 표시한다. 이 API는 인기 도시 선정 기능을 제공하지 않는다.
- 국가를 선택하면 해당 `countryId`를 API-LOC-2에 전달한다.

## 언어 정책

기존 `Accept-Language` 헤더를 유지한다. 지원 언어 중 요청 우선순위에 맞는 언어를 적용하며, 헤더가 없거나 지원 언어가 매칭되지 않으면 서비스 기본 언어를 사용한다. 지원 언어 목록 및 기본값은 별도 확정한다. 국가 표시명과 응답 메시지에 적용하며, ID는 번역하지 않는다.
