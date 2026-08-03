# [DOM-2] 취향 정보

## 도메인 요약

| 항목 | 내용 |
| :--- | :--- |
| 도메인명 | 취향 정보 |
| Domain ID | DOM-2 |
| 목적 | 사용자의 여행 취향을 구조화하여 AI 코스 생성과 개인화 추천에 재사용한다. |
| 생성 방식 | 사진 메타데이터 기반 행동 분석 |
| 주요 소비처 | 여행 코스 생성, 개인화 추천, 선호도 기반 장소/활동 필터링 |


## 데이터 모델

| 필드명 | 타입 | 필수 | 설명 | 예시 |
| :--- | :--- | :--- | :--- | :--- |
| `tasteProfileId` | UUID | Y | 취향 프로필 고유 식별자 | `550e8400-e29b-41d4-a716-446655440001` |
| `userId` | UUID | Y | 사용자 고유 식별자 | `550e8400-e29b-41d4-a716-446655440000` |
| `updatedAt` | date | Y | 취향 프로필 마지막 갱신일 | `2026-07-13` |
| `travelPurpose` | object | Y | 여행 목적별 선호 점수 | `{ "relaxation": 4 }` |
| `travelPaceDensity` | enum | Y | 여행 속도/일정 밀도 | `balanced` |
| `preferredLocationType` | object | Y | 장소 유형별 선호 점수 | `{ "beachResort": 5 }` |
| `activityPreference` | object | Y | 활동 유형별 선호 점수 | `{ "photographyVideo": 5 }` |
| `spendingTendency` | enum | Y | 소비 취향 | `cost_effective` |
| `companionType` | enum | Y | 동행 형태 | `friends` |
| `foodPreference` | object | Y | 음식 취향별 선호 점수 | `{ "cafeDessert": 5 }` |
| `seasonalEnvironmentPreference` | string[] | Y | 계절/환경 선호 목록 | `["warm_region"]` |


## 점수형 필드 공통 규칙

점수형 필드는 모두 `1~5` 범위의 정수로 저장한다.

| 점수 | 의미 |
| :--- | :--- |
| `1` | 선호도가 매우 낮음 |
| `2` | 선호도가 낮음 |
| `3` | 보통 |
| `4` | 선호도가 높음 |
| `5` | 선호도가 매우 높음 |


## 점수형 필드 상세


### `travelPurpose`

| 키 | 라벨 | 설명 |
| :--- | :--- | :--- |
| `relaxation` | 휴양형 | 쉬고 재충전하는 여행 |
| `sightseeing` | 관광형 | 유명 명소와 랜드마크 중심 |
| `culturalExperience` | 문화체험형 | 역사, 전통, 현지 문화 중심 |
| `gourmet` | 미식형 | 음식점, 시장, 카페 탐방 중심 |
| `natureExploration` | 자연탐방형 | 산, 바다, 숲, 국립공원 중심 |
| `activity` | 액티비티형 | 등산, 서핑, 스키, 다이빙 등 |
| `shopping` | 쇼핑형 | 쇼핑몰, 아웃렛, 기념품 중심 |
| `festivalEvent` | 축제·이벤트형 | 공연, 스포츠, 지역 축제 중심 |
| `wellness` | 웰니스형 | 스파, 요가, 명상, 온천 중심 |
| `selfDevelopment` | 자기계발형 | 어학, 워케이션, 교육 프로그램 중심 |


### `preferredLocationType`

| 키 | 라벨 | 설명 |
| :--- | :--- | :--- |
| `bigCity` | 대도시형 | 대도시 중심 여행 선호 |
| `smallTownAlley` | 소도시·골목형 | 소도시와 골목 탐방 선호 |
| `natureHinterland` | 자연·오지형 | 자연 중심의 한적한 장소 선호 |
| `beachResort` | 해변·휴양지형 | 바다와 휴양지 중심 여행 선호 |
| `mountainPlateau` | 산악·고원형 | 산악, 고원, 트레킹 지역 선호 |
| `historicalCity` | 역사도시형 | 역사와 문화 자원이 많은 도시 선호 |
| `themeParkResort` | 테마파크·리조트형 | 테마파크와 복합 리조트 선호 |
| `famousSpotPreferred` | 유명 관광지 선호형 | 검증된 유명 명소 선호 |
| `hiddenSpotPreferred` | 숨은 명소 선호형 | 덜 알려진 장소와 로컬 스팟 선호 |


### `activityPreference`

| 키 | 라벨 | 설명 |
| :--- | :--- | :--- |
| `viewing` | 관람형 | 박물관, 미술관, 공연 관람 선호 |
| `experience` | 체험형 | 공방, 요리, 전통문화 체험 선호 |
| `adventure` | 모험형 | 익스트림 스포츠, 트레킹 선호 |
| `photographyVideo` | 사진·영상형 | 사진과 영상 기록 중심 활동 선호 |
| `gourmetExploration` | 미식 탐방형 | 맛집, 시장, 카페 탐방 선호 |
| `nightlife` | 밤문화형 | 야간 활동과 나이트라이프 선호 |
| `shopping` | 쇼핑형 | 쇼핑 활동 선호 |
| `relaxation` | 휴식형 | 휴식 중심 활동 선호 |
| `localInteraction` | 현지인 교류형 | 현지인과의 교류 및 로컬 경험 선호 |


### `foodPreference`

| 키 | 라벨 | 설명 |
| :--- | :--- | :--- |
| `localFoodActive` | 현지 음식 적극 체험형 | 현지 음식을 적극적으로 경험 |
| `famousRestaurantCentered` | 유명 맛집 중심형 | 유명 맛집 방문 선호 |
| `streetFood` | 길거리 음식형 | 시장과 길거리 음식 선호 |
| `cafeDessert` | 카페·디저트형 | 카페와 디저트 탐방 선호 |
| `fineDining` | 파인다이닝형 | 고급 레스토랑 경험 선호 |
| `familiarFoodPreferred` | 익숙한 음식 선호형 | 새로운 음식보다 익숙한 음식 선호 |
| `dietaryRestriction` | 식단 제한형 | 채식, 할랄, 알레르기 등 제한 고려 필요 |
| `sightseeingOverFood` | 관광 우선형 | 음식보다 관광을 더 중시 |


## 선택형 필드 정의


### `travelPaceDensity`

| 저장값 | 표시 라벨 | 설명 |
| :--- | :--- | :--- |
| `slow_stay` | 느긋한 체류형 | 한 지역에 오래 머무름 |
| `balanced` | 균형형 | 관광과 휴식을 적절히 배분 |
| `dense_schedule` | 빡빡한 일정형 | 짧은 시간에 많은 장소 방문 |
| `spontaneous` | 즉흥형 | 현장에서 일정을 결정 |
| `long_stay` | 장기여행형 | 몇 주 이상 머무르며 생활하듯 여행 |


### `spendingTendency`

| 저장값 | 표시 라벨 | 설명 |
| :--- | :--- | :--- |
| `cost_effective` | 가성비형 | 가격 대비 만족도 중시 |
| `moderate` | 중간 소비형 | 보편적인 예산 수준 선호 |
| `luxury` | 럭셔리형 | 고급 호텔, 파인다이닝, 전용 서비스 선호 |


### `companionType`

| 저장값 | 표시 라벨 |
| :--- | :--- |
| `solo` | 혼자 여행형 |
| `couple` | 연인 여행형 |
| `friends` | 친구 여행형 |
| `family` | 가족 여행형 |
| `with_children` | 아이 동반형 |
| `with_parents` | 부모님 동반형 |
| `group` | 단체 여행형 |
| `with_pet` | 반려동물 동반형 |
| `social` | 새로운 사람과 어울리는 여행형 |


### `seasonalEnvironmentPreference`

| 저장값 | 표시 라벨 |
| :--- | :--- |
| `warm_region` | 따뜻한 지역 선호형 |
| `cold_region` | 추운 지역 선호형 |
| `summer_resort` | 여름 휴양형 |
| `winter_sports` | 겨울 스포츠형 |
| `spring_flower_autumn_foliage` | 봄꽃·가을 단풍형 |
| `dry_weather` | 건조한 날씨 선호형 |
| `off_season` | 비수기 여행형 |
| `peak_season` | 성수기 분위기 선호형 |


## 예시 데이터

```json
{
  "tasteProfileId": "550e8400-e29b-41d4-a716-446655440001",
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "updatedAt": "2026-07-13",
  "travelPurpose": {
    "relaxation": 4,
    "sightseeing": 3,
    "culturalExperience": 3,
    "gourmet": 5,
    "natureExploration": 4,
    "activity": 2,
    "shopping": 2,
    "festivalEvent": 1,
    "wellness": 3,
    "selfDevelopment": 1
  },
  "travelPaceDensity": "balanced",
  "preferredLocationType": {
    "bigCity": 3,
    "smallTownAlley": 4,
    "natureHinterland": 4,
    "beachResort": 5,
    "mountainPlateau": 2,
    "historicalCity": 3,
    "themeParkResort": 1,
    "famousSpotPreferred": 3,
    "hiddenSpotPreferred": 5
  },
  "activityPreference": {
    "viewing": 3,
    "experience": 4,
    "adventure": 2,
    "photographyVideo": 5,
    "gourmetExploration": 5,
    "nightlife": 2,
    "shopping": 2,
    "relaxation": 4,
    "localInteraction": 3
  },
  "spendingTendency": "cost_effective",
  "companionType": "friends",
  "foodPreference": {
    "localFoodActive": 5,
    "famousRestaurantCentered": 4,
    "streetFood": 4,
    "cafeDessert": 5,
    "fineDining": 2,
    "familiarFoodPreferred": 2,
    "dietaryRestriction": 1,
    "sightseeingOverFood": 2
  },
  "seasonalEnvironmentPreference": [
    "warm_region",
    "spring_flower_autumn_foliage",
    "off_season"
  ]
}
```
