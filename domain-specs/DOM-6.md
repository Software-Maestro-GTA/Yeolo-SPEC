# [DOM-6] 여행 코스 친구 초대 프로세스

# **코스 공유 링크 — 딥링크 처리 구현 계획**

> 관련: TSK-40 (#49) / API-SHARE-1·2·3 / DOM-6 대상: FE · 앱 · 인프라 · BE 상태: **BE의 공유 API는 구현·배포 완료. 링크를 눌렀을 때의 앱/스토어 분기는 미구현.**


## **1. 배경 — 지금 어디까지 되어 있나**

BE는 공유 링크의 **발급·조회·수락 API**를 제공하며 dev에 배포되어 있다.

```plain text
① 소유자 앱   POST /api/courses/{courseId}/share-links   BE 응답    { "shareUrl": "https://<도메인>/share/<token>",                "shareToken": "<token>",                "expiresAt": "2026-08-17T00:00:00Z" }   ← 기본 7일② FE         shareUrl 을 OS 공유 시트로 친구에게 전달        ← BE 개입 없음③ 친구가 링크 클릭   ⛔ 현재 여기서 끊긴다 — 링크 도메인에 아무것도 없어 브라우저가 빈 페이지를 연다④ 앱이 링크에서 토큰 추출   GET  /api/share-links/{shareToken}   ← 인증 불필요, 미리보기⑤ 로그인 후 수락           POST /api/share-links/{shareToken}/accept   → 코스가 GET /api/courses 목록에 나타난다
```

①·④·⑤는 동작한다. **③만 비어 있다.**

BE가 딥링크에 관여하는 부분은 URL 문자열 조립 한 줄이 전부다.

```java
// ShareLinkPropertiesreturn base+"/"+ shareToken;// base = share-link.base-url
```

`share-link.base-url` 의 현재 기본값 `https://yeolo.app/share` 는 **자리표시자**이며 아무도 서빙하지 않는다.


## **2. 무엇을 만들어야 하나**

iOS **Universal Links** / Android **App Links** 는 커스텀 스킴(`yeolo://`)이 아니라 **평범한 https URL** 을 쓴다. 앱이 설치돼 있으면 OS 가 가로채 앱을 열고, **없으면 브라우저가 그 URL 을 그대로 연다.** 따라서 "앱 없으면 스토어로" 를 만들려면 **그 주소에 실제 웹 페이지가 있어야 한다.**

성립 조건 3가지:

| **#** | **필요한 것** | **담당** |
| :--- | :--- | :--- |
| 1 | `https://<도메인>/.well-known/apple-app-site-association` | FE/인프라 |
| 2 | `https://<도메인>/.well-known/assetlinks.json` | FE/인프라 |
| 3 | `https://<도메인>/share/<token>` 폴백 페이지 (스토어 유도) | FE |

여기에 앱 측 설정(Associated Domains / intent-filter)이 있어야 1·2가 의미를 갖는다.


## **3. 채택안 — A안 (FE/인프라가 랜딩 서빙)**

**BE 는 링크 문자열만 만들고, 링크 도메인의 응답은 FE/인프라가 책임진다.**

  - 랜딩은 성격상 정적 웹 자산이며, BE 도메인·배포 주기와 분리하는 편이 맞다.
  - BE 는 현재 `@RestController`(`/api/**`)만 가진 구조라, 웹 페이지 응답 책임을 들이지 않는다.
  - BE 작업량이 설정 1줄(또는 CORS 1개)로 끝난다.
> 반려안 (B안): BE 가 `GET /share/{token}` 리다이렉트와 `.well-known` 파일까지 서빙. FE 배포를 기다리지 않아도 되지만, 링크 도메인이 BE 도메인에 묶이고 BE 가 웹 페이지 책임을 진다. FE 리소스를 당장 붙일 수 없을 때만 재검토한다.


### **3-1. 먼저 정해야 할 갈림길 — 랜딩을 정적으로 둘 것인가 SSR 로 둘 것인가**

이 선택이 **BE 작업 유무를 결정한다.**

|  | **정적 (S3 + 브라우저 JS)** | **SSR (Lambda@Edge · Next.js 등)** |
| :--- | :--- | :--- |
| 미리보기 데이터 | 브라우저가 `GET /api/share-links/{token}` 호출 | 서버가 호출 |
| **BE CORS 작업** | **필요** | 불필요 |
| **카카오톡 OG 미리보기** | ❌ 불가 (크롤러는 JS 를 실행하지 않는다) | ✅ 코스 제목·목적지를 OG 태그로 노출 |

**SSR 권장.** 링크를 카카오톡으로 뿌리는 것이 주 시나리오이므로 OG 미리보기 유무의 체감 차이가 크다.


## **4. 선행 조건 (양쪽 공통)**

착수 전에 아래가 확정되어야 한다.

  - [ ] **딥링크 도메인** (예: `https://yeolo.app`)
  - [ ] iOS `TEAM_ID` · `BUNDLE_ID`
  - [ ] Android `PACKAGE_NAME` · **릴리스 서명 SHA-256 지문**
  - [ ] App Store · Play Store URL (앱 배포 후 확정)
> Play 앱 서명을 쓰는 경우 지문은 업로드 키가 아니라 **Play Console 이 발급한 앱 서명 키** 의 것이어야 한다. 여기서 가장 자주 틀린다.


## **5. BE 파트**


### **5-1. 링크 도메인 교체 — 코드 변경 없음**

```plain text
share-link.base-url=${SHARE_LINK_BASE_URL:https://yeolo.app/share}share-link.ttl=${SHARE_LINK_TTL:P7D}      # 0 이하면 무기한(expiresAt: null)
```

확정 도메인을 dev/prod 환경변수에 넣으면 끝난다. 이미 외부 주입 가능하게 되어 있다.


### **5-2. CORS — 정적 랜딩을 택할 때만**

현재 응답에 `Access-Control-*` 헤더가 하나도 없어 브라우저 JS 의 교차 출처 호출은 전부 차단된다. 추가한다면 **최소 범위로** 연다.

```java
// SecurityConfig.cors(Customizer.withDefaults())@BeanCorsConfigurationSource corsConfigurationSource(ShareLinkProperties props){    CorsConfiguration c=new CorsConfiguration();    c.setAllowedOrigins(props.allowedOrigins());// 랜딩 도메인만. "*" 금지    c.setAllowedMethods(List.of("GET"));// 미리보기는 GET 뿐    c.setAllowCredentials(false);// 무인증 API — 열 이유가 없다    UrlBasedCorsConfigurationSource s=new UrlBasedCorsConfigurationSource();    s.registerCorsConfiguration("/api/share-links/*", c);// 미리보기 경로만return s;}
```

의도적으로 좁힌 지점 셋:

  1. **수락(****`/accept`****)은 열지 않는다** — 앱에서 호출하므로 브라우저 CORS 가 필요 없다.
  1. `allowCredentials=false` — 미리보기는 토큰을 싣지 않는다.
  1. 허용 origin 을 환경변수로 뺀다 — 도메인이 정해지기 전에도 구현해 둘 수 있다.
검증: preflight 200 과 **인증 API 에는 CORS 가 열리지 않았다**는 것을 `@WebMvcTest` 로 고정한다.


### **5-3. Android 설치 후 복원**

Play Store URL 에 `&referrer=<shareToken>` 을 붙이는 것은 **랜딩 페이지가** 한다. BE 추가 작업 없음.

**BE 작업량: SSR 이면 설정 1줄, 정적이면 CORS 1개(약 30분 + 테스트).**


## **6. FE 파트**


### **6-1. ****`/.well-known/apple-app-site-association`**

확장자 없음 · `Content-Type: application/json` · **리다이렉트 금지** · HTTPS 필수.

```json
{"applinks":{"details":[{"appIDs":["<TEAM_ID>.<BUNDLE_ID>"],"components":[{"/":"/share/*","comment":"코스 공유 링크"}]}]}}
```


### **6-2. ****`/.well-known/assetlinks.json`**

```json
[{"relation":["delegate_permission/common.handle_all_urls"],"target":{"namespace":"android_app","package_name":"<PACKAGE_NAME>","sha256_cert_fingerprints":["<릴리스 서명 SHA-256>"]}}]
```


### **6-3. ****`/share/:token`**** 랜딩 페이지**

앱이 설치된 사용자는 OS 가 가로채므로 **이 페이지는 미설치자만 본다.**

```plain text
1) User-Agent 판별     iOS      → App Store     Android  → Play Store  (+ &referrer=<token>)     데스크톱  → "모바일에서 열어주세요" + 코스 요약2) 코스 요약 표시 — GET /api/share-links/{token}3) iOS 미설치자에게 "설치 후 이 링크를 다시 열어주세요" 안내
```

에러 문구는 DOM-6 §예외 상황을 그대로 쓴다.

| **응답** | **화면 문구** |
| :--- | :--- |
| `404` 유효하지 않은 공유 링크 | 유효하지 않은 공유 링크입니다. |
| `404` 코스 없음 (소유자가 삭제) | 공유된 여행 코스를 찾을 수 없습니다. |
| `410` 만료·회수 | 만료된 공유 링크입니다. 친구에게 다시 초대를 요청해주세요. |

미리보기 응답 스키마 (API-SHARE-2):

```json
{"status":200,"message":"여행 코스 공유 링크 조회 성공","data":{"course":{"title":"...","destinationCountry":"...","destinationCity":"...","startDate":"2026-09-01","totalDays":4},"inviter":{"displayName":"...|null","profileImageUrl":"...|null"},"expiresAt":"2026-08-17T00:00:00Z|null"}}
```

> `courseId` 는 의도적으로 내려주지 않는다 (DOM-6 §보안 및 운영 정책 — 실제 courseId 를 링크·미리보기에 노출하지 않는다). 수락(API-SHARE-3) 응답에서 처음 받는다.


## **7. 앱 파트**

  - iOS: `Associated Domains` entitlement 에 `applinks:<도메인>`
  - Android: `intent-filter` + `android:autoVerify="true"`
  - 링크 수신 → 토큰 추출 → 미리보기 호출 → **비로그인이면 토큰을 보관한 채 로그인** → 복귀 후 수락 (DOM-6 §비로그인 사용자 처리 — 로그인 전후로 초대 정보가 유지되어야 한다)
  - 수락 응답의 `courseId` 로 코스 상세 화면(API-COURSE-2)으로 이동

### **자기 자신의 코스 / 이미 수락한 링크**

API-SHARE-3 는 두 경우 모두 **400 ****`수락할 수 없는 공유 링크입니다.`** 로 정의한다. 정상 동작이며, 앱은 이 400 을 오류가 아니라 "이미 내 목록에 있음" 으로 안내하는 편이 자연스럽다.

> DOM-6 은 이 상황에서 "기존 코스 상세로 이동" 을 권하지만, 400 응답에는 `courseId` 가 없어 이동할 대상을 알 수 없다. 명세 간 모순이며 Notion 원본 확인이 필요하다. (경위: `docs/spec-index.md` §"미해소 명세 모순")


## **8. 인프라 파트**

  - CloudFront 에서 `/.well-known/*` 와 `/share/*` 를 랜딩 오리진으로 라우팅
  - **AASA 에 리다이렉트가 끼면 iOS 검증이 실패한다** — 301/302 없이 200 으로 직접 응답해야 한다
  - `SHARE_LINK_BASE_URL` 을 dev/prod 시크릿·환경변수에 추가

## **9. 순서와 검증**

```plain text
① 도메인 확정            → BE: SHARE_LINK_BASE_URL 반영            (즉시 가능)② 앱 식별자 수집         → .well-known 두 파일 배포③ 앱: Associated Domains / intent-filter 추가 후 재설치④ 랜딩 페이지 배포       (+ 정적 방식이면 BE CORS 함께)⑤ 검증
```

```bash
# AASA — 200 + application/json + 리다이렉트 없어야 한다curl -sI https://<도메인>/.well-known/apple-app-site-association# Android App Links 공식 검증curl -s"https://digitalassetlinks.googleapis.com/v1/statements:list\?source.web.site=https://<도메인>&relation=delegate_permission/common.handle_all_urls"# 실기기adb shell am start -a android.intent.action.VIEW -d"https://<도메인>/share/<token>"
```


## **10. 함정 모음**

  - **AASA 는 앱 설치 시점에 캐시된다.** 파일을 고쳤는데 앱이 안 열리면 앱을 지웠다 다시 설치해야 한다.
  - **Firebase Dynamic Links 는 2025-08 종료됐다.** 검색하면 가장 먼저 나오지만 쓸 수 없다.
  - **iOS 는 설치 후 초대 복원(deferred deep link)의 공식 방법이 없다.** Branch·AppsFlyer 같은 서드파티를 붙이거나, "설치 후 링크를 다시 열어주세요" 안내로 처리한다. 공유 토큰이 7일 유효하므로 재클릭 방식으로 충분하다. 초대 수락률이 중요해지면 그때 재검토한다.
  - **Android 는 Play Install Referrer 로 해결된다.** 스토어 URL 의 `&referrer=<token>` 을 설치 후 앱이 읽는다. 표준이고 무료다.
  - **공유 링크는 발급할 때마다 새 토큰이 나온다.** 서버가 토큰을 해시로만 저장해(Refresh Token 과 같은 정책) 기존 링크의 평문을 되돌려줄 수 없기 때문이다. 이전 링크도 만료 전까지 함께 유효하다.
  - **소유자가 원본 코스를 삭제하면** 그 코스의 공유 권한과 발급된 링크가 모두 정리된다. 이후 링크를 열면 "공유된 여행 코스를 찾을 수 없습니다"(404) 가 나온다.

## **11. 결정이 필요한 항목**

  - [ ] 랜딩을 **정적 / SSR** 중 어느 쪽으로 할 것인가 (BE CORS 작업 유무가 갈림)
  - [ ] 딥링크 도메인
  - [ ] iOS deferred deep link 를 서드파티로 해결할 것인가, 재클릭 안내로 갈 것인가
  - [ ] 공유 링크 만료 7일이 적절한가 (`SHARE_LINK_TTL` 로 조정 가능, 0 이면 무기한)

## 목적

여행 코스 확인 화면에서 사용자가 생성한 여행 코스를 친구에게 링크로 공유하고, 초대받은 사용자가 해당 링크를 통해 코스를 자신의 여행 코스 목록에 추가할 수 있도록 한다.

이 문서는 API 상세가 아니라 **사용자 플로우, 화면 전환, 권한 정책, 예외 상황**을 중심으로 정의한다.


## 핵심 사용자 시나리오


### 시나리오 1. 코스 생성자가 친구에게 여행 코스를 공유한다

1. 사용자는 여행 코스 확인 화면에서 생성된 코스를 확인한다.
1. 사용자는 코스가 마음에 들면 `친구 초대` 버튼을 선택한다.
1. 앱은 공유 가능한 링크를 준비한다.
1. 사용자는 OS 공유 시트를 통해 친구에게 링크를 전달한다.
1. 공유가 완료되면 사용자는 기존 여행 코스 확인 화면에 머무른다.

### 시나리오 2. 초대받은 사용자가 공유 링크를 연다

1. 초대받은 사용자는 친구에게 받은 공유 링크를 클릭한다.
1. 앱이 설치되어 있으면 앱으로 이동하고, 설치되어 있지 않으면 앱 설치 화면으로 이동한다.
1. 앱은 공유 링크에서 초대 정보를 확인한다.
1. 초대받은 사용자가 로그인되어 있지 않으면 로그인 화면으로 이동한다.
1. 로그인 완료 후 앱은 기존에 열었던 공유 링크 흐름으로 돌아온다.
1. 앱은 공유받은 여행 코스의 요약 정보를 보여준다.
1. 사용자는 공유 코스를 자신의 목록에 추가할지 결정한다.

### 시나리오 3. 초대받은 사용자가 공유 코스를 수락한다

1. 사용자는 공유 코스 미리보기 화면에서 `내 코스에 추가` 또는 `수락` 버튼을 선택한다.
1. 앱은 공유 코스를 사용자의 여행 코스 목록에 추가한다.
1. 사용자는 추가된 코스의 상세 화면으로 이동한다.
1. 이후 사용자는 여행 코스 목록 화면에서 공유받은 코스를 다시 확인할 수 있다.

## 화면 흐름

```plain text
[코스 생성자]
여행 코스 확인 화면
→ 친구 초대 선택
→ 공유 링크 생성
→ OS 공유 시트
→ 친구에게 링크 전달
→ 여행 코스 확인 화면 유지

[초대받은 사용자]
공유 링크 클릭
→ 앱 실행
→ 로그인 여부 확인
→ 비로그인 시 로그인
→ 공유 코스 미리보기
→ 수락
→ 여행 코스 상세 화면
→ 여행 코스 목록에서 재확인
```


## 비로그인 사용자 처리

공유 링크를 클릭한 사용자가 로그인되어 있지 않은 경우에도 공유 흐름이 끊기지 않아야 한다.

```plain text
공유 링크 클릭
→ 초대 정보 임시 보관
→ 로그인 화면 이동
→ OAuth 로그인 완료
→ 보관된 초대 정보 복원
→ 공유 코스 미리보기
→ 수락
→ 코스 상세 화면 이동
```

로그인 과정에서 공유 링크 정보가 사라지면 사용자가 다시 링크를 눌러야 하므로, 앱은 로그인 전후로 초대 정보를 유지해야 한다.


## 공유 코스 미리보기 화면

초대받은 사용자가 링크를 열었을 때 바로 코스를 목록에 추가하기보다, 먼저 코스 요약을 보여주는 것이 좋다.

공유 코스 미리보기 화면에는 다음 정보를 제공한다.

- 코스 제목
- 여행 국가
- 여행 도시
- 여행 시작일
- 여행 기간
- 초대한 사용자 이름
- 수락 버튼
- 취소 또는 뒤로가기 버튼
미리보기 화면의 목적은 사용자가 어떤 코스를 공유받았는지 이해한 뒤 수락할 수 있게 하는 것이다.


## 권한 정책


### 코스 생성자

코스 생성자는 다음 동작을 할 수 있다.

- 자신이 생성한 여행 코스 조회
- 자신이 생성한 여행 코스 삭제
- 여행 코스 공유 링크 생성
- 친구에게 공유 링크 전달

### 공유받은 사용자

공유받은 사용자는 다음 동작을 할 수 있다.

- 공유 링크 열기
- 공유 코스 미리보기 확인
- 공유 코스 수락
- 공유받은 코스 상세 조회
- 여행 코스 목록에서 공유받은 코스 확인
- 공유받은 코스를 자신의 목록에서 제거
공유받은 사용자가 코스를 목록에서 제거하더라도 원본 여행 코스는 삭제되지 않는다.  

즉, 공유받은 사용자의 삭제 동작은 **원본 삭제가 아니라 자신의 목록에서 제거**하는 동작이다.


## 코스 목록에서의 처리

공유받은 코스를 수락하면 해당 코스는 여행 코스 목록 화면에 표시된다.

이번 스프린트에서는 코스 목록에서 소유 코스와 공유받은 코스를 반드시 구분하지 않아도 된다.  

다만 추후 구분이 필요해지면 `내가 만든 코스`, `공유받은 코스`와 같은 표시를 추가할 수 있다.


## 예외 상황


### 공유 링크가 유효하지 않은 경우

사용자가 잘못된 링크나 손상된 링크를 열면 앱은 다음 안내를 제공한다.

```plain text
유효하지 않은 공유 링크입니다.
```

이 경우 사용자는 이전 화면으로 돌아가거나 홈/코스 목록 화면으로 이동할 수 있다.


### 공유 링크가 만료된 경우

공유 링크에 만료 정책이 있는 경우, 만료된 링크를 열면 다음 안내를 제공한다.

```plain text
만료된 공유 링크입니다.
친구에게 다시 초대를 요청해주세요.
```


### 공유된 코스가 삭제된 경우

코스 생성자가 원본 코스를 삭제한 뒤 초대받은 사용자가 링크를 열면 다음 안내를 제공한다.

```plain text
공유된 여행 코스를 찾을 수 없습니다.
```


### 이미 수락한 링크인 경우

사용자가 이미 수락한 공유 링크를 다시 열면 중복으로 코스를 추가하지 않는다.

이 경우 앱은 기존에 추가된 코스 상세 화면 또는 여행 코스 목록 화면으로 이동시키는 것이 좋다.


### 자기 자신의 코스를 수락하려는 경우

코스 생성자가 자신이 만든 공유 링크를 직접 열면 별도의 수락 절차 없이 기존 코스 상세 화면으로 이동하는 것이 자연스럽다.


## 보안 및 운영 정책

- 공유 링크에는 실제 `courseId`를 직접 노출하지 않는다.
- 공유 링크는 서버에서 관리하는 임시 초대 식별자를 기반으로 처리한다.
- 앱은 Google Place ID나 Google API Key를 직접 다루지 않는다.
- 장소 정보와 좌표는 서버에서 정리된 값을 받아 사용한다.
- 공유받은 사용자의 삭제 동작은 원본 삭제가 아니라 접근 권한 제거로 처리한다.
- 같은 사용자가 같은 공유 링크를 여러 번 수락해도 중복으로 코스가 추가되지 않아야 한다.
- 공유 링크는 필요 시 만료 시간을 가질 수 있다.
