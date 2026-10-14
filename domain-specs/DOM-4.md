# [DOM-4] 취향 분석 프로세스

## 1. 한눈에 보는 취향 분석

사용자가 동의한 사진의 **위치·촬영 시간 메타데이터**를 분석해 여행 취향을 만든다. 사진 원본이나 픽셀은 분석하지 않는다.

AI는 사진을 방문 단위로 묶고, **LLM에 한 번 요청**하여 전체 취향을 생성한 뒤 코드로 근거를 보정한다. 계절·환경 선호는 **최소 1개**를 제공한다.

```plain text
FE 대표 사진 메타데이터 수집
→ BE 장소·시간 전처리
→ AI 방문 통계 생성
→ LLM 1회로 전체 취향 생성
→ 코드로 점수·계절 선호 보정
→ SSE로 tasteProfile 반환
```

| 담당 | 역할 |
| :--- | :--- |
| Yeolo-FE | 동의를 확인하고 날짜·위치가 분산된 대표 메타데이터를 수집한다. |
| BE | 좌표·시간을 장소·계절 정보로 전처리한다. 결과 저장과 프로필 ID 발급을 담당한다. |
| Yeolo-AI | 방문 집계, 단일 LLM 분석, 근거 보정과 응답 생성을 담당한다. |


## 2. 단계별 처리


### ① 대표 메타데이터 수집 — FE

휴대폰 사진 보관함에서 **위치·시간이 유효한 대표 기록**을 고른다. 원본 사진을 업로드하는 과정이 아니라, 서버의 방문 분석에 필요한 메타데이터를 수집하는 과정이다.

| 순서 | 처리 |
| :--- | :--- |
| 1. 동의·권한 | 온보딩에서 분석 동의를 저장한 뒤 사진 읽기 권한을 요청한다. 일부 사진만 허용하면 그 범위에서 수집한다. |
| 2. 기간별 조회 | 최근 **365일**을 **12개 기간**으로 나눠 이미지 자산을 조회한다. 기간별 최신 **250개**, 전체 최대 **3,000개**를 후보로 확인한다. |
| 3. 위치·시간 검증 | 각 자산의 **생성 시각·위도·경도**를 읽는다. 중복 ID, 누락·잘못된 좌표나 시각, 범위 밖 기록은 제외한다. |
| 4. 촬영 묶음 축소 | 같은 UTC 날짜에서 대표 위치 **100m 이내·대표 시각부터 2시간 이내**의 사진을 근사 방문으로 묶어 **1개**를 남긴다. |
| 5. 대표 표본 구성 | 하루 최대 **5개**, 날짜별 1개 우선 및 기간 간 순환 선택으로 최종 **최대 100개**를 구성한다. |
| 6. 전송 여부 확인 | 대표 기록 **5개 이상·서로 다른 UTC 날짜 3일 이상**이면 시간순 메타데이터를 BE로 전송한다. 부족하면 요청하지 않고 안내한다. |

전송 필드는 `sourceImageId`, `capturedAt`, `latitude`, `longitude`, `timezone`이다. `capturedAt`은 현재 구현에서 자산 생성 시각을 UTC로 변환한 값이며, `timezone`의 기본값도 UTC다.

FE는 **좌표·시간으로 대표 표본을 선택**하고, AI는 BE가 만든 **장소 정보로 방문을 재집계**한다. FE의 근사 방문을 실제 장소 방문이나 전체 방문 빈도로 확정하지 않는다. 일부 사진 접근 상태에서 표본이 부족하면 사진 추가 선택을 위한 설정 이동을 안내한다.


### ② 장소·시간 전처리 — BE

FE는 사진 ID, 촬영 시각, 위도·경도를 보낸다. BE는 이를 다음 정보로 가공하여 AI에 `userId`와 `items`로 전달한다.

- **장소:** 국가, 도시, 지역, 행정구역, 장소명, 장소 유형.
- **시간:** 촬영 시각, 요일, 주말 여부, 시간대, 계절.
BE 전처리는 API 명세상 역할이다. BE 구현 자체는 이 문서의 코드 검증 범위에 포함하지 않는다.


### ③ 방문 통계 생성 — AI

무효 기록과 사진 ID 중복을 제외하고, **같은 장소·같은 날짜에서 첫 사진부터 2시간 이내**의 사진을 한 방문으로 묶는다. 다른 날짜 또는 2시간 이후의 기록은 별도 방문이다.

한 방문에서 같은 유형이 여러 번 등장해도 근거는 1회만 센다. 예를 들어 같은 카페에서 사진 20장을 찍어도 카페 방문 근거는 1회다.

방문 수, 날짜·장소 다양성, 장소 유형·계절 분포와 취향 항목별 방문 근거를 JSON 통계로 만든다. **사진 개수 자체는 선호 강도의 근거로 사용하지 않는다.**


### ④ 전체 취향 생성 — LLM 1회

방문 통계만 단일 LLM 체인에 전달하여 아래 8개 영역을 한 번에 생성한다. 별도 요약·병렬 채점·추가 LLM 평가 요청은 하지 않는다.

| 영역 | 결과 |
| :--- | :--- |
| `travelPurpose` | 여행 목적 10개 점수 |
| `preferredLocationType` | 장소 유형 9개 점수 |
| `activityPreference` | 활동 9개 점수 |
| `foodPreference` | 음식 8개 점수 |
| `travelPaceDensity` | 일정 밀도 |
| `spendingTendency` | 소비 성향 |
| `companionType` | 동행 형태 |
| `seasonalEnvironmentPreference` | 계절·환경 선호 목록, 최소 1개 |

점수는 1~5 정수, 선택형 값은 기존 도메인의 enum을 사용한다. 사진 ID·사용자 ID·개별 촬영 시각·장소명 목록은 LLM에 보내지 않는다. MBTI, 결제 내역, 실제 동행자 정보도 분석 입력에 포함되지 않는다.


### ⑤ 근거 보정 및 결과 반환 — AI

LLM 결과에 코드 보정을 적용한다. 점수와 계절 선택 규칙은 아래 3절을 따른다.

최종 `tasteProfile`을 SSE로 반환하고, 근거·잠정값 사유는 내부 LangSmith trace에 기록한다.


## 3. 결과를 결정하는 규칙


### 점수: 반복 근거가 있을 때만 높은 점수 유지

| 관측 근거 | 최종 처리 |
| :--- | :--- |
| 해당 유형 3방문 이상이고 서로 다른 날짜 2일 이상 | LLM의 4~5점을 유지할 수 있다. |
| 근거가 없거나 반복 기준 미달 | 3점으로 보정한다. |
| LLM이 1~2점 반환 | 3점으로 보정한다. 방문 기록만으로 싫어함을 확정하지 않는다. |

**3점은 중립·미확정이며, 기록이 없다는 이유로 비선호를 뜻하지 않는다.**

야간 촬영만으로 밤문화를 높이지 않는다. bar/night_club 같은 장소 유형이 필요하다. 일반 restaurant만으로 현지식·유명 맛집·파인다이닝을 확정하지 않는다.

사진 자체 취향, 현지인 교류, 식단 제한, 익숙한 음식, 대도시·골목, 유명·숨은 명소, 음식보다 관광 중시 등 직접 근거가 없는 항목도 3점과 사용자 확인 대상으로 처리한다.


### 동행·소비·일정: 호환 기본값 사용

사진 메타데이터로 확인할 수 없는 값은 `companionType=solo`, `spendingTendency=moderate`, `travelPaceDensity=balanced`를 반환한다. **실제로 확인한 사용자 취향이 아닌 호환 기본값**이다.


### 계절·환경: 근거 순서대로 최소 1개 선택

코드가 다음 우선순위로 최종 목록을 결정한다. LLM의 빈 목록이나 불일치 선택에 의존하지 않는다.

1. **반복 활동 근거가 있으면:** 3방문·2일 기준을 만족한 아래 후보를 모두 선택한다.
1. **약한 활동 근거만 있으면:** 관측된 후보 중 방문 수와 날짜 수가 가장 큰 1개를 잠정 선택한다.
1. **활동 근거도 없으면:** 가장 많이 관측된 촬영 계절로 UI용 잠정값 1개를 선택한다.
| 활동 근거 | 선택 후보 |
| :--- | :--- |
| 여름 beach/resort_hotel 방문 | `summer_resort` — 여름 휴양형 |
| 겨울 ski_resort 방문 | `winter_sports` — 겨울 스포츠형 |
| 봄·가을 botanical_garden 방문 | `spring_flower_autumn_foliage` — 봄꽃·가을 단풍형 |

활동 근거가 없을 때의 잠정값은 여름 → `warm_region`, 겨울 → `cold_region`, 봄·가을 → `spring_flower_autumn_foliage`다.

**잠정값은 UI에 최소 한 항목을 제공하기 위한 정책이다. 실제 기후·활동 선호를 입증하지 않는다.** 식물원 방문 역시 꽃·단풍 관람 목적을 확정하는 정보는 아니다.

기후·날씨·목적지별 성수기 자료가 없어 `dry_weather`, `off_season`, `peak_season`은 확정하지 않는다. 전체 허용 enum은 취향 정보 문서를 따른다.


## 4. 응답과 오류 처리

`POST /internal/ai/taste-profile/analysis`를 사용하며, `/behavior` 별칭과 `X-Internal-Api-Key` 인증을 유지한다.

| 상태 | 처리 |
| :--- | :--- |
| 분석 중 | SSE `progress`, step=`ANALYZING_PREFERENCE` |
| 성공 | SSE `complete`, data에는 `tasteProfile`만 포함 |
| 유효한 기록 없음 | 스트림·LLM 호출 전에 HTTP 400 |
| 인증 실패 | HTTP 401 |
| LLM·구조화 출력·결과 처리 실패 | SSE `error`. 이후 complete를 반환하지 않음 |

내부 `analysisMetadata`에는 통계, 항목별 근거, confidence, 기본값·잠정값 사유, 사용자 확인 대상을 기록한다. **공개 응답에는 포함하지 않는다.**

confidence의 low/medium은 근거 휴리스틱이며 정확도 확률이 아니다. 추적이 비활성화되면 LangSmith에 원격 저장되지 않는다. 현재 FE/BE는 프로필만으로 잠정값을 구분할 수 없어 사용자 확인·표시 연동은 후속 작업이다.

저장과 `tasteProfileId`, `userId`, `updatedAt` 발급은 BE가 담당한다.


## 5. 검증 결과와 남은 과제

**2026-10-03 AI 검증:** Ruff와 전체 pytest **522개 통과**, 취향 분석 회귀 테스트 **45개 통과**.

실제 Gemini·LangSmith 합성 테스트 **3건**에서 각각 LLM 호출 1회와 정상 SSE 완료, 내부 근거 저장을 확인했다.

- 여름 카페 1건: 잠정 `warm_region`.
- 여름 해변 3방문·3일: `summer_resort`.
- 전체 프로필: 사진 49개 → 32개 방문. 8개 영역·36개 점수와 51개 규칙·계약 검사 통과. API 응답 9.64초, 3,277토큰.
전체 프로필에서는 미식·카페 5점, 문화체험·밤문화·쇼핑·웰니스 4점이 나왔다. 1회 관측된 파인다이닝은 3점으로 보정됐다.

**이 검증은 실행과 보정 규칙의 확인이며 실제 사용자 취향 정확도 평가는 아니다.**

후속 과제는 다음과 같다.

- 실제 사용자 확인값으로 점수·계절 잠정값과 반복 실행 안정성을 평가한다.
- 사진 선택 편향과 생활·여행 기록 혼재를 고려하고 방문·근거 기준을 조정한다.
- 안정적인 장소 ID, 촬영 장소 시간대와 FE·BE·AI 시간 정합성을 확인한다.
- 사용자 확인값 우선 반영과 UI 잠정값 표시를 연동한다.
현재 사용자별 모델 학습이나 기존 프로필의 누적 갱신 기능은 없다.


## 6. 개발 참고

<details><summary>FE 수집 상세 및 검증 기록</summary>

현재 Yeolo-FE 소스코드 기준이다. 수집 정책은 초기 휴리스틱이며 실제 취향 정확도를 보장하지 않는다.


### 실행 경로와 기기 접근

- 온보딩의 `PhotoConsentScreen`에서 `agreed=true`, `consentVersion=v1.0`을 서버에 저장한다. 저장 성공 후 분석 화면으로 이동한다.
- `useTasteAnalysisPipeline.runPipeline()`이 `fetchPhotosWithExifData()`를 호출한다. 수집 함수는 Expo `requestPermissionsAsync(false, ['photo'])`로 사진 읽기 권한을 요청하며, 거부되면 수집을 중단한다.
- `accessPrivileges=limited`도 허용된 사진 안에서 처리한다. 분석 동의와 운영체제의 사진 접근 권한은 별개다.

### 후보 탐색과 메타데이터 추출

- 수집 시작 시각을 고정하고 최근 365일을 12개 동일 길이 구간으로 나눈다. 달력상 월이 아니라 약 30.4일 구간이며 기간 경계는 중복되지 않는다.
- Expo `Query`에서 `MediaType.IMAGE`와 기간별 `AssetField.CREATION_TIME` 조건을 적용한다. 생성 시간 내림차순으로 `offset`을 이동하며 페이지당 최대 100개, 기간당 최대 250개를 읽는다. GPS 없는 페이지 이후에도 다음 페이지와 다른 기간을 탐색하며 전체 후보 상한은 3,000개다.
- 자산 `getCreationTime()`으로 epoch milliseconds를 읽고, 유효한 경우 `getLocation()`으로 좌표를 읽는다. 자산 최대 4개를 동시에 처리한다.
- ID가 없거나 이미 읽은 ID는 제외한다. 시각이 누락·비유한·최근 365일 범위 밖·미래인 경우, 좌표가 누락·비유한·위도 ±90 또는 경도 ±180 범위 밖인 경우도 제외한다. 좌표 0은 허용한다.
- 개별 자산 조회 오류는 건너뛰고 계속하며 보관함 쿼리 실패는 분석을 중단한다. 생성 시간이 실제 촬영 EXIF와 일치하는지는 별도 검증 대상이다.

### 촬영 묶음과 최종 표본

- UTC 날짜별로 시간순 처리한다. 같은 시각이면 사진 ID로 순서를 정한다.
- 기존 대표 위치에서 100m 이내이고 대표 시각부터 2시간 이내이면 해당 묶음에 포함하여 추가 대표를 만들지 않는다. 대표 기준점을 이동하지 않아 시간·거리 연결이 무한히 확장되지 않는다.
- 다른 날짜의 같은 장소 또는 2시간을 초과한 기록은 별도 후보로 남긴다. 사진 내용의 중복 검사나 실제 장소 ID 판정은 하지 않는다.
- 기간별 날짜 묶음에서 후보가 5개를 넘으면 시간순 기록의 시작·끝을 포함하여 균등 선택한다. 최종 전송에도 UTC 날짜당 5개 상한을 적용한다.
- 기간 안에서는 날짜별로 1개를 먼저 선택한 뒤 두 번째 기록을 선택한다. 기간 간에는 최근 기간부터 순환 선택하여 최종 100개까지 구성하고 시간순으로 정렬한다.

### FE → BE 전송 계약

`POST /api/users/me/taste-profile/analysis`에 `Content-Type: application/json`, JWT Bearer 인증으로 전송한다. 대표 기록만 `images` 배열에 담고 사진 파일·픽셀·기기 파일 경로는 넣지 않는다.

| 필드 | 실제 값의 출처 |
| :--- | :--- |
| `sourceImageId` | 기기 미디어 자산의 `asset.id` |
| `capturedAt` | 자산 생성 시각을 `toISOString()`으로 변환한 UTC 시각 |
| `latitude`, `longitude` | 선택된 자산의 위치 메타데이터 |
| `timezone` | 수집 함수 인자. 현재 분석 화면은 기본값 `UTC`를 사용 |

아래는 배열 항목 일부를 보여주는 예시다. 실제 요청은 대표 기록 5개 이상과 UTC 날짜 3일 이상 조건을 충족해야 한다.

```json
{
  "images": [
    {
      "sourceImageId": "example-asset-id",
      "capturedAt": "2026-09-01T03:00:00.000Z",
      "latitude": 37.5665,
      "longitude": 126.978,
      "timezone": "UTC"
    }
  ]
}
```


### 오류 안내와 적용 경계

- 전체 접근일 때 사진 없음, 위치·시간 없음, 대표 표본 부족을 구분하여 안내한다. 대표 5개 또는 UTC 날짜 3일 기준을 충족하지 않으면 BE 분석 API를 호출하지 않는다.
- 일부 사진 접근에서 부족하면 사진 추가 선택 안내와 설정 이동 버튼을 제공한다. 권한 거부에도 설정 이동을 제공하며 전체 접근을 강제하지 않는다.
- FE 좌표 기반 묶음과 AI 장소 키 기반 집계의 방문 수·의미는 다르다. 날짜·기간·전송 상한이 있는 표본을 전체 방문 빈도로 해석하면 안 된다.
- UTC 날짜와 AI 입력 offset·현지 장소 시간의 정합성은 BE 연동에서 확인해야 한다. 현재 기기 시간대를 과거 촬영 장소의 시간대로 대체하지 않는다.
- 기간별 최신 250개 제한으로 이전 기록이 누락될 수 있고 생활·업무·여행 기록을 자동 구분하지 않는다. 인접 장소가 합쳐지거나 긴 체류가 여러 묶음으로 나뉠 수 있으며 사진 공백을 체류 시간으로 해석하지 않는다.
- 수집 로그는 후보·유효·대표·날짜·실패 개수만 남긴다. 좌표·사진 ID·원본 네이티브 오류는 새 수집 로그에 기록하지 않는다.

### 코드와 검증

- 수집: `packages/app/src/services/photoService.ts`. 대표 선택: `packages/app/src/services/photoSelection.ts`.
- 정책: `packages/app/src/constants/config.ts`의 `APP_CONFIG.PHOTO_SAMPLING` 및 `ANALYSIS_PHOTO_LIMIT`.
- 실행·전송: `packages/app/src/hooks/useTasteAnalysisPipeline.ts`, `packages/common/src/api/taste.ts`. 동의·오류 화면: `PhotoConsentScreen.tsx`, `TasteAnalysisScreen.tsx`.
- 검증 기록: 사진 서비스 회귀 테스트 15개 및 화면의 요청 차단·설정 버튼 검사 포함, 앱 전체 Jest 28 suites/238 tests, TypeScript·변경 파일 Prettier·Git 공백 검사 통과.
- Airbridge 저장소 수정 후 ARM64 Android Debug APK 빌드도 통과했다. 빌드 성공은 실제 기기 수집·전송 검증을 의미하지 않는다. 네이티브 보관함 테스트는 모킹했으며 실제 iOS/Android 보관함과 사용자 취향 정확도는 미검증이다.
</details>

<details><summary>AI 집계·선택·추적 상세</summary>

- 빈 사진 ID, timezone 없는·파싱 불가·UTC 범위 밖 시각, 빈 장소명·unknown 등을 제외한다. 같은 ID의 내용이 충돌하면 정렬된 JSON으로 한 레코드를 결정한다.
- 국가·도시·지역·행정구역·장소명은 NFKC·공백 축약·casefold로 정규화한다. 날짜·시간대는 입력 offset을 사용하고 장소의 실제 timezone을 별도 조회하지 않는다. 같은 이름의 지점·명칭 변경을 완전히 구분하지 못한다.
- 방문별 장소 유형은 합집합이다. `FIELD_TYPES`는 항목별 근거 매핑이며 `matchedPlaceTypes`는 조건에 맞게 실제 관측된 유형만 기록한다. 유형 통계를 상위 10개로 자르지 않는다.
- 요일·주말·시간대는 방문 대표 시각에서 다시 계산한다. 00–05시 dawn, 06–11시 morning, 12–17시 afternoon, 18–21시 evening, 22–23시 night다. 계절은 BE의 season을 유지한다.
- 통계: 사진 input/unique/duplicate/invalid/valid 개수, visitCount, distinctDayCount, distinctPlaceCount, 요일·주말·시간대·계절·도시 분포, 유형별 방문·날짜 수, 항목별 방문·날짜 수 및 매칭 유형.
- `dataSufficiency`: 10일 이상이면서 15곳 이상이면 sufficient, 나머지는 provisional. AI 분석을 막는 최소 조건이 아니며 FE 요청 기준·항목별 반복 근거와 별개다.
- 약한 활동 동률은 방문 수 → 날짜 수 → summer_resort/winter_sports/spring_flower_autumn_foliage 순서다. 촬영 계절 동률은 spring/summer/autumn/winter 순서다. 입력 순서에 의존하지 않고 중복 없이 선택한다.
- 분석 전용 스키마는 계절 목록 최소 길이 1을 요구한다. 과거 빈 배열을 포함한 코스 입력 호환성을 위해 공유 취향 스키마의 입력 허용 범위는 유지한다.
- 통계 속 유형·도시 문자열은 데이터로 취급하며 포함된 명령을 따르지 않는다.
- 내부 trace metadata: statistics, fieldEvidence, fallbackFields, requiresUserConfirmation. 잠정 선택에 fallbackReason·selectionReason과 선택 계절 근거를 기록한다. 추적 기록 실패로 정상 분석을 중단하지 않는다.
- 방문 2시간·반복 근거 3회/2일·표본 충분성 10일/15곳은 초기 휴리스틱이다. 장소 유형 방문이 이용 목적을 확정하지 않으며 실제 사용자 평가로 조정해야 한다.
</details>


## 관련 문서와 구현

- 취향 결과 도메인: [취향 정보](https://app.notion.com/p/3911d7341cda80679169f4b58a9da359)
- FE–BE 분석 API: [취향 분석](https://app.notion.com/p/3911d7341cda8028902ce908c0d10791)
- BE–AI 분석 API: [취향 분석](https://app.notion.com/p/3911d7341cda806b94eef019769865ae)
- [단일 호출·계절 최소 선택 구현 PR #45](https://github.com/Software-Maestro-GTA/Yeolo-AI/pull/45)
- [전체 프로필 실제 LLM 검증 보고서](https://github.com/Software-Maestro-GTA/Yeolo-AI/blob/codex/taste-profile-single-call/docs/taste-analysis/live-verification-full-profile-2026-10-03/report.md)
- AI 코드: `app/services/behavior_statistics.py`, `behavior_evidence.py`, `behavior_service.py`; `app/agent/prompts.py`, `taste_profile_chains.py`; `app/schemas/behavior.py`, `taste_profile.py`; `app/api/taste_profile.py`.
- 회귀 테스트: `tests/test_behavior_statistics.py`, `test_behavior_evidence.py`, `test_behavior_analysis.py`. 검증 명령: `bash .agents/hooks/test.sh`.
- 로컬 설명: `docs/taste-analysis/README.md`. 이전 4회 호출 검증 기록은 과거 구조의 실행 결과다.
