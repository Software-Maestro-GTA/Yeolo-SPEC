# [API-MRT-6] 상품 제휴 링크 생성

## 1. 기본 정보

- **Method**: `POST`
- **Endpoint**: `/api/myrealtrip/links`
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
  "targetUrl": "[https://experiences.myrealtrip.com/products/example](https://experiences.myrealtrip.com/products/example)"
}
```

## 3. Response 사양

### 성공 응답 (Status 200)
```json
{
  "status": 200,
  "message": "상품 제휴 링크 생성 성공",
  "data": {
    "url": "[https://myrealt.rip/example](https://myrealt.rip/example)"
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

상품 제휴 링크 생성 기능을 Yeolo Server API로 제공한다. Client는 검색 조건 또는 원본 URL만 보내고, Server가 마이리얼트립 파트너 API를 호출한다.


## 요청

`POST /api/myrealtrip/links`

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
| targetUrl | string | 필수 | 검색 응답에서 받은 productUrl. 항공 오류 시 기존 홈 이동에는 [https://www.myrealtrip.com/도](https://www.myrealtrip.com/%EB%8F%84) 사용할 수 있다. |

Request Body 예시:

```json
{
  "targetUrl": "https://experiences.myrealtrip.com/products/example"
}
```


## 처리 규칙

- 상품 클릭 시 호출하며 상품 원본 URL을 제휴 추적용 링크로 변환한다. Client가 API 키를 사용하거나 제휴 링크를 직접 조합하지 않는다.
- 문자열 포함 검사가 아니라 URL 파서로 검증한다. HTTPS, 정확한 [myrealtrip.com](http://myrealtrip.com/) 호스트 또는 .[myrealtrip.com](http://myrealtrip.com/)으로 끝나는 서브도메인만 허용한다.
- 사용자정보·명시적 포트가 있는 URL, HTTP, [myrealtrip.com](http://myrealtrip.com/).evil.example 등의 유사 도메인은 400이다. Server는 입력 URL을 임의 HTTP 요청 대상으로 사용하지 않고 고정된 파트너 mylink API의 targetUrl 값으로만 전달한다.
- 성공 URL도 HTTPS의 [myrealt.rip](http://myrealt.rip/) 호스트인지 검증하고 응답한다. 잘못된 공급자 응답은 502이다.
- Client는 반환 URL을 외부 브라우저로 연다. 일반 원본 URL을 바로 여는 선택은 가능하지만 현재 제휴 추적 동작을 유지하려면 이 API를 사용한다.

## 성공 응답

```json
{
  "status": 200,
  "message": "상품 제휴 링크 생성 성공",
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

- 현재 FE 어댑터가 사용하는 파트너 경로: `POST /v1/mylink`. 상위 호스트: `https://partner-ext-api.myrealtrip.com`. FE→BE Method와 파트너 Method는 다를 수 있다.
- 파트너 요청에만 Server 환경변수의 키를 `Authorization: Bearer {MY_REAL_TRIP_API_KEY}`로 사용한다. Yeolo 사용자 토큰을 파트너에 전달하지 않는다.
- [[마이리얼트립] 마케팅파트너 Open API 접속 IP 등록 안내](https://app.notion.com/p/40c1d7341cda803cadf8d3204a09c350): 등록된 공인 IP에서 파트너 API를 호출하도록 안내되어 있어, 등록된 Server 송신 IP를 사용해야 한다. IP 제출과 등록 완료는 별개이므로 실제 연동 가능 여부는 구현 시 확인한다.
- 현재 구현 근거: `packages/common/src/api/myrealtrip.ts`, `packages/app/src/services/bookingService.ts`, `packages/app/src/screens/BookingScreen.tsx`.
