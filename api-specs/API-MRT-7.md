# [API-MRT-7] 쿠폰 정보 전송

## 1. 기본 정보

- **Method**: `GET`
- **Endpoint**: `/api/myrealtrip/coupons`
- **통신 방식**: REST
- **인증 필요**: Y
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
  "message": "쿠폰 정보 조회 성공",
  "data": {
    "coupons": [
      {
        "code": "EXAMPLE1000",
        "minimumPrice": 50000,
        "discount": 1000
      }
    ]
  }
}
```

### Error Codes
401: Yeolo access token 누락, 유효하지 않거나 만료된 토큰
426: 지원하지 않는 앱 버전
429: 요청 한도 초과
500: 서버 내부 오류

### 실패 응답
```json
{
  "status": 500,
  "message": "쿠폰 정보를 불러오지 못했습니다.",
  "data": null
}
```

## 4. 상세 내용 및 예외 케이스

## 작성 상태

Client → Server 이관을 위한 구현 요청 초안이다. API ID·경로·Method·인증 정책은 이번 제안이며 배포 완료를 의미하지 않는다. 현재 로그인 후 사용하는 예약 흐름에 맞춰 Yeolo 로그인 사용자 인증을 필수로 한다. Server에서 access token을 검증하고 사용자별 요청 제한을 적용한다.


## 기능

쿠폰 정보 전송 기능을 Yeolo Server API로 제공한다. 앱에 고정된 쿠폰 설정을 서버에서 관리한다.


## 요청

`GET /api/myrealtrip/coupons`

공통 헤더는 [API 명세서](https://app.notion.com/p/3911d7341cda808c812deeeb162ac88d)를 따른다. 마이리얼트립 API 키는 Client에서 받지 않으며 응답에도 포함하지 않는다.

```json
{
  "Authorization": "Bearer {accessToken}",
  "Accept-Language": "ko",
  "X-App-Version": "{appVersion}"
}
```

Path Params, Query Params, Request Body는 없다.


## 처리 규칙

- 현재 앱의 MYREALTRIP_TICKET_COUPONS 상수를 Server 관리 데이터로 이전한다. 공개 프로모션 코드 목록 조회이며 개인 쿠폰 발급·사용·검증 API가 아니다.
- 현재 투어·티켓 화면에 필요한 code, minimumPrice, discount만 반환한다. 금액은 원화 정수이며 code는 중복되지 않는다.
- Server는 관리 중인 활성 쿠폰만 표시 순서대로 반환한다. 만료되었거나 비활성화된 쿠폰은 제외하고, 노출할 쿠폰이 없으면 200과 [data.coupons](http://data.coupons/): []를 반환한다.
- Client는 코드를 복사해 마이리얼트립 결제 화면에서 입력하도록 안내한다. 최소 구매액 충족만으로 실제 적용 가능함을 보장하지 않는다.
- 기존 앱의 실제 코드·금액은 서버 초기 데이터 후보이며 적용 기간·활성 여부는 운영 확인 후 등록한다. 응답 예시의 EXAMPLE1000은 가상의 코드다.
- 마이리얼트립 Open API에 쿠폰 조회 기능이 존재한다고 가정하지 않는다. 이 API는 Yeolo Server가 관리하는 쿠폰 설정을 반환한다.

## 성공 응답

```json
{
  "status": 200,
  "message": "쿠폰 정보 조회 성공",
  "data": {
    "coupons": [
      {
        "code": "EXAMPLE1000",
        "minimumPrice": 50000,
        "discount": 1000
      }
    ]
  }
}
```

예시는 구조 설명용 가상 상품·가격·식별자·URL이며 실제 판매 또는 예약 가능함을 뜻하지 않는다.


## 실패 응답

```json
{
  "status": 500,
  "message": "쿠폰 정보를 불러오지 못했습니다.",
  "data": null
}
```

- 401: Yeolo access token 누락, 유효하지 않거나 만료된 토큰
- 500: 서버 내부 오류

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

- Yeolo Server의 운영 설정 또는 저장소에서 조회한다. 파트너 API 호출은 필요하지 않다.
- [[마이리얼트립] 마케팅파트너 Open API 접속 IP 등록 안내](https://app.notion.com/p/40c1d7341cda803cadf8d3204a09c350): 등록된 공인 IP에서 파트너 API를 호출하도록 안내되어 있어, 등록된 Server 송신 IP를 사용해야 한다. IP 제출과 등록 완료는 별개이므로 실제 연동 가능 여부는 구현 시 확인한다.
- 현재 구현 근거: `packages/common/src/api/myrealtrip.ts`, `packages/app/src/services/bookingService.ts`, `packages/app/src/screens/BookingScreen.tsx`, `packages/app/src/constants/config.ts`, `packages/app/src/components/booking/TicketCouponPack.tsx`.
