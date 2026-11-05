# [API-MRT-5] 항공 검색 제휴 링크 생성

## 1. 기본 정보

- **Method**: `POST`
- **Endpoint**: `/api/myrealtrip/flights/link`
- **통신 방식**: REST
- **인증 필요**: Y
- **Success Status**: `200`

## 2. Request 사양

### Header
{
  "Authorization": "Bearer {accessToken}",
  "Content-Type": "application/json",
  "Accept-Language": "ko",
  "X-App-Version": "{appVersion}"
}

### Path Params
없음

### Query Params
없음

### Request Body
```json
{
  "depAirportCd": "ICN",
  "arrAirportCd": "NRT",
  "depDate": "2026-12-10",
  "arrDate": "2026-12-12",
  "adult": 2
}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "항공 검색 링크 생성 성공",
  "data": {
    "url": "[https://myrealt.rip/example](https://myrealt.rip/example)"
  }
}
```

### Error Codes
400: 입력값 오류 또는 지원하지 않는 항공 검색 조건
401: Yeolo access token 누락, 유효하지 않거나 만료된 토큰
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

항공 검색 제휴 링크 생성 기능을 Yeolo Server API로 제공한다. Client는 검색 조건 또는 원본 URL만 보내고, Server가 마이리얼트립 파트너 API를 호출한다.


## 요청

`POST /api/myrealtrip/flights/link`

공통 헤더는 [API 명세서](https://app.notion.com/p/3911d7341cda808c812deeeb162ac88d)를 따른다. 마이리얼트립 API 키는 Client에서 받지 않으며 응답에도 포함하지 않는다.

```json
{
  "Authorization": "Bearer {accessToken}",
  "Content-Type": "application/json",
  "Accept-Language": "ko",
  "X-App-Version": "{appVersion}"
}
```

| 필드 | 타입 | 필수 여부 | 규칙 |
| :--- | :--- | :--- | :--- |
| depAirportCd | string | 필수 | 선택한 출발 공항 코드. 대문자 영문 3자리. |
| arrAirportCd | string | 필수 | 선택한 도착 공항 코드. 출발 공항과 달라야 한다. |
| depDate | string | 필수 | YYYY-MM-DD 형식의 유효한 출국 날짜. |
| arrDate | string | 필수 | YYYY-MM-DD 형식의 유효한 귀국 날짜. depDate와 같거나 이후. |
| adult | integer | 필수 | 1 이상 성인 수. |

Request Body 예시:

```json
{
  "depAirportCd": "ICN",
  "arrAirportCd": "NRT",
  "depDate": "2026-12-10",
  "arrDate": "2026-12-12",
  "adult": 2
}
```


## 처리 규칙

- 현재 기능은 왕복 항공 검색 페이지로 이동하는 링크 생성이다. 항공편 목록·실시간 운임 조회 응답이 아니다.
- Server가 tripTypeCd: RT를 추가해 항공 검색 랜딩 URL을 생성하고, 그 URL을 mylink API로 변환한 최종 제휴 URL만 반환한다.
- 과거 출국 날짜·날짜 역전·동일 공항·잘못된 인원은 400이다. 공급자가 지원하지 않는 검색 조건 또는 노선도 사용자에게 구분 가능한 메시지의 400으로 처리한다.
- 랜딩 URL과 제휴 URL은 Server에서 검증한다. 랜딩 URL은 HTTPS 및 [myrealtrip.com](http://myrealtrip.com/) 또는 그 서브도메인, 최종 제휴 URL은 HTTPS 및 [myrealt.rip](http://myrealt.rip/)만 허용한다. 사용자정보와 명시적 포트가 있는 URL은 거절한다.
- Client는 data.url을 외부 브라우저로 연다. 현재 왕복·성인만 지원하며 편도·다구간·소아·유아 확장은 별도 요구사항으로 다룬다.
- 날짜는 시각이 없는 날짜 문자열로 전달한다. 본 초안의 과거 날짜 판정 기준은 서비스 기준일 Asia/Seoul이며, Client와 Server에서 동일하게 적용한다.

## 성공 응답

```json
{
  "status": 200,
  "message": "항공 검색 링크 생성 성공",
  "data": {
    "url": "https://myrealt.rip/example"
  }
}
```

예시는 구조 설명용 가상 상품·가격·식별자·URL이며 실제 판매 또는 예약 가능함을 뜻하지 않는다.


## 실패 응답

```json
{
  "status": 400,
  "message": "요청 값을 확인해주세요.",
  "data": null
}
```

- 400: 입력값 오류 또는 지원하지 않는 항공 검색 조건
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

- 현재 FE 어댑터가 사용하는 파트너 경로: `POST /v1/products/flight/fare-query-landing-url → POST /v1/mylink`. 상위 호스트: `https://partner-ext-api.myrealtrip.com`. FE→BE Method와 파트너 Method는 다를 수 있다.
- 파트너 요청에만 Server 환경변수의 키를 `Authorization: Bearer {MY_REAL_TRIP_API_KEY}`로 사용한다. Yeolo 사용자 토큰을 파트너에 전달하지 않는다.
- [[마이리얼트립] 마케팅파트너 Open API 접속 IP 등록 안내](https://app.notion.com/p/40c1d7341cda803cadf8d3204a09c350): 등록된 공인 IP에서 파트너 API를 호출하도록 안내되어 있어, 등록된 Server 송신 IP를 사용해야 한다. IP 제출과 등록 완료는 별개이므로 실제 연동 가능 여부는 구현 시 확인한다.
- 현재 구현 근거: `packages/common/src/api/myrealtrip.ts`, `packages/app/src/services/bookingService.ts`, `packages/app/src/screens/BookingScreen.tsx`.
