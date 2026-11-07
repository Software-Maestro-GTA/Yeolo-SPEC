# [API-MRT-3] 숙소 조회

## 1. 기본 정보

- **Method**: `GET`
- **Endpoint**: `/api/myrealtrip/hotels`
- **통신 방식**: REST
- **인증 필요**: N
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Authorization": "Bearer {accessToken}",
  "Accept-Language": "ko",
  "X-App-Version": "{appVersion}"
}

### Path Params
없음

### Query Params
{
  "regionId": 12345,
  "checkIn": "2026-12-10",
  "checkOut": "2026-12-12",
  "adultCount": 2,
  "page": 1
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
  "message": "숙소 조회 성공",
  "data": {
    "items": [
      {
        "itemName": "숙소 이름 예시",
        "productUrl": "[https://accommodation.myrealtrip.com/union/products/example](https://accommodation.myrealtrip.com/union/products/example)",
        "salePrice": 120000,
        "imageUrl": null,
        "starRating": 4,
        "reviewScore": 4.5,
        "reviewCount": 120
      }
    ],
    "page": 1,
    "totalCount": 1,
    "hasMore": false
  }
}
```

### Error Codes
400: 입력값 오류
401: Yeolo access token 누락, 유효하지 않거나 만료된 토큰
426: 지원하지 않는 앱 버전
429: 요청 한도 초과
500: 서버 내부 오류 또는 파트너 키 설정 누락
502: 파트너 인증/IP 거절, 호출 실패 또는 잘못된 응답
504: 파트너 응답 시간 초과

### 실패 응답
```json
{
  "status": 400,
  "message": "요청 값을 확인해주세요.",
  "data": null
}
```

## 4. 상세 내용 및 예외 케이스

## 작성 상태

Client → Server 이관을 위한 구현 요청 초안이다. API ID·경로·Method·인증 정책은 이번 제안이며 배포 완료를 의미하지 않는다. 현재 로그인 후 사용하는 예약 흐름에 맞춰 Yeolo 로그인 사용자 인증을 필수로 한다. Server에서 access token을 검증하고 사용자별 요청 제한을 적용한다.


## 기능

숙소 조회 기능을 Yeolo Server API로 제공한다. Client는 검색 조건 또는 원본 URL만 보내고, Server가 마이리얼트립 파트너 API를 호출한다.


## 요청

`GET /api/myrealtrip/hotels`

공통 헤더는 [API 명세서](https://app.notion.com/p/3911d7341cda808c812deeeb162ac88d)를 따른다. 마이리얼트립 API 키는 Client에서 받지 않으며 응답에도 포함하지 않는다.

```json
{
  "Authorization": "Bearer {accessToken}",
  "Accept-Language": "ko",
  "X-App-Version": "{appVersion}"
}
```

| 필드 | 타입 | 필수 여부 | 규칙 |
| :--- | :--- | :--- | :--- |
| regionId | integer | 필수 | 숙박 지역 검색에서 선택한 식별자. |
| checkIn | string | 필수 | YYYY-MM-DD 형식의 유효한 체크인 날짜. |
| checkOut | string | 필수 | YYYY-MM-DD 형식의 유효한 체크아웃 날짜. checkIn보다 이후. |
| adultCount | integer | 필수 | 1 이상 성인 수. 소수·음수·문자열 오류는 400. |
| page | integer | 선택 | 1 이상. 기본값 1. 페이지당 20개 고정. |

Query Params 예시:

```json
{
  "regionId": 12345,
  "checkIn": "2026-12-10",
  "checkOut": "2026-12-12",
  "adultCount": 2,
  "page": 1
}
```


## 처리 규칙

- 숙박 지역명이나 여행 일정 전체 대신 선택한 regionId·기간·성인 수만 받는다. 과거 체크인 날짜와 날짜 역전은 400으로 처리한다.
- FE→BE page는 1부터 시작한다. 현재 FE 어댑터 기준 숙박 상위 API는 0부터 시작하므로 Server가 upstreamPage = page - 1로 변환한다. 이 규칙은 상위 계약 확인 후 구현한다.
- 객실·예약 상세 조회, 결제는 이번 이관 범위에 포함하지 않는다. 상품 클릭 시 상품 제휴 링크 생성 API를 호출한다.
- 날짜는 시각이 없는 날짜 문자열로 전달한다. 본 초안의 과거 날짜 판정 기준은 서비스 기준일 Asia/Seoul이며, Client와 Server에서 동일하게 적용한다.

## 성공 응답

```json
{
  "status": 200,
  "message": "숙소 조회 성공",
  "data": {
    "items": [
      {
        "itemName": "숙소 이름 예시",
        "productUrl": "https://accommodation.myrealtrip.com/union/products/example",
        "salePrice": 120000,
        "imageUrl": null,
        "starRating": 4,
        "reviewScore": 4.5,
        "reviewCount": 120
      }
    ],
    "page": 1,
    "totalCount": 1,
    "hasMore": false
  }
}
```

예시는 구조 설명용 가상 상품·가격·식별자·URL이며 실제 판매 또는 예약 가능함을 뜻하지 않는다.


### 상품 및 페이지 필드

| 필드 | 타입 | 설명 |
| :--- | :--- | :--- |
| items | array | 현재 페이지 상품 목록. 결과가 없으면 빈 배열. |
| items[].itemName | string | 상품명. |
| items[].productUrl | string | 검증된 HTTPS 마이리얼트립 원본 URL. 현재 Client의 목록 식별·중복 제거에도 사용. |
| items[].salePrice | number | 0 이상 유한한 숫자. 현재 화면의 원화 표시 기준을 유지하며 최종 결제가는 별도 확인. |
| items[].imageUrl | string 또는 null | 선택 이미지. 미제공 시 null 또는 생략. |
| items[].starRating | number 또는 null | 선택 숙박 등급. 리뷰 평점과 구분. |
| items[].reviewScore | string, number 또는 null | 선택 리뷰 평점. 현재 Client 타입 유지. |
| items[].reviewCount | integer 또는 null | 선택 리뷰 수. |
| page | integer | Client가 요청한 1부터 시작하는 페이지 번호. |
| totalCount | integer 또는 null | 상위 API가 제공한 전체 건수. 미제공 시 null. |
| hasMore | boolean | 추가 페이지 존재 여부. |

- Client가 사용하지 않는 category, tags, priceDisplay와 공급자 내부 메타데이터는 반환하지 않는다.
- 페이지 크기는 20개로 고정한다. 상위 API가 전체 건수를 제공하면 이를 그대로 사용해 추가 페이지 여부를 판단한다. 미제공 시 totalCount는 null이며, 원본 페이지가 20개면 hasMore: true로 반환하고 다음 빈 페이지에서 종료한다. 가짜 전체 건수를 생성하지 않는다.
- totalCount가 null일 때 Client는 정확한 전체 건수 표시를 생략한다. 이는 현재 BookingHotelPage/BookingTicketPage의 totalCount: number에서 nullable로 바꾸어야 하는 제안이다.
- 상품명·원본 URL·가격이 유효하지 않은 항목은 제외한다. hasMore 판단은 필터링 전 공급자 페이지 기준으로 한다. 필수 배열 자체가 없거나 응답 구조가 잘못되면 빈 결과로 숨기지 않고 502를 반환한다.
- 가격은 조회 시점의 참고값이며 최종 요금과 예약 조건은 마이리얼트립에서 확인한다.

## 실패 응답

```json
{
  "status": 400,
  "message": "요청 값을 확인해주세요.",
  "data": null
}
```

- 400: 입력값 오류
- 401: Yeolo access token 누락, 유효하지 않거나 만료된 토큰
- 429: 요청 한도 초과
- 500: 서버 내부 오류 또는 파트너 키 설정 누락
- 502: 파트너 인증/IP 거절, 호출 실패 또는 잘못된 응답
- 504: 파트너 응답 시간 초과
- 공급자의 401·403은 Server의 파트너 인증 또는 등록 IP 문제로 처리해 502로 변환한다. 이를 Client의 로그인 만료로 전달하지 않는다. 키·토큰·공급자 원문 오류는 공개 응답에 포함하지 않는다.
- 공급자 또는 Yeolo의 요청 제한은 429로 전달하며 재시도 시점을 알 수 있으면 Retry-After 헤더를 반환한다.

## 로그인 인증

- Client → Yeolo Server: 로그인으로 발급받은 Yeolo access token을 `Authorization: Bearer {accessToken}`으로 전달한다. 비밀번호·refresh token·userId를 이 API의 인증값으로 보내지 않는다.
- Server는 파트너 호출 또는 쿠폰 조회 전에 토큰의 서명·만료·유효성을 검증하고 인증된 사용자 식별자를 얻는다. 토큰이 없거나 유효하지 않거나 만료되면 401을 반환한다.
- Client는 기존 공통 HTTP 클라이언트의 토큰 주입 및 토큰 재발급 흐름을 사용한다. 재발급 후에도 인증에 실패하면 재로그인을 안내한다.
- Server → 마이리얼트립: Server 환경변수의 파트너 API 키를 별도의 Authorization 헤더로 사용한다. Yeolo 사용자 access token을 마이리얼트립으로 전달하지 않는다. 쿠폰 조회는 파트너 호출이 필요 없다.
- Accept-Language는 기존 공통 클라이언트 언어 헤더를 따른다. 공급자가 다국어 상품 검색·응답을 지원한다고 가정하지 않는다. X-App-Version은 실제 배포 앱 버전을 전달한다.

### 인증 실패 응답 (401)

```json
{
  "status": 401,
  "message": "인증이 필요합니다.",
  "data": null
}
```


## 서버 연동 및 근거

- 현재 FE 어댑터가 사용하는 파트너 경로: `POST /v1/products/accommodation/search`. 상위 호스트: `https://partner-ext-api.myrealtrip.com`. FE→BE Method와 파트너 Method는 다를 수 있다.
- 파트너 요청에만 Server 환경변수의 키를 `Authorization: Bearer {MY_REAL_TRIP_API_KEY}`로 사용한다. Yeolo 사용자 토큰을 파트너에 전달하지 않는다.
- [[마이리얼트립] 마케팅파트너 Open API 접속 IP 등록 안내](https://app.notion.com/p/40c1d7341cda803cadf8d3204a09c350): 등록된 공인 IP에서 파트너 API를 호출하도록 안내되어 있어, 등록된 Server 송신 IP를 사용해야 한다. IP 제출과 등록 완료는 별개이므로 실제 연동 가능 여부는 구현 시 확인한다.
- 현재 구현 근거: `packages/common/src/api/myrealtrip.ts`, `packages/app/src/services/bookingService.ts`, `packages/app/src/screens/BookingScreen.tsx`.
