# [DOM-1] 성향 정보 (Taste Profile)

개인 여행 성향 분석 결과를 저장하는 도메인입니다. 사용자의 설문 응답 또는 행동 데이터 분석 결과를 정규화된 성향 프로필로 저장하고, 이후 여행 코스 생성 요청에서 재사용합니다.

---

## 1. 주요 필드 정의

- `tasteProfileId`: 성향 프로필 고유 식별자 (UUID)
- `userId`: 사용자 고유 식별자 (UUID)
- `sourceType`: 성향 생성 방식 (`survey`, `behavior`, `mixed`)
- `updatedAt`: 성향 프로필 마지막 갱신일
- `travelPurpose`: 여행 목적 선호도
- `travelPaceDensity`: 여행 속도/일정 밀도
- `preferredLocationType`: 선호 장소 유형
- `activityPreference`: 활동 취향
- `spendingTendency`: 소비 성향
- `companionType`: 동행 형태
- `foodPreference`: 음식 취향
- `seasonalEnvironmentPreference`: 계절/환경 취향

---

## 2. 저장 목적

- 사용자의 여행 목적, 장소, 활동, 음식, 예산, 동행 성향을 구조화한다.
- AI 코스 생성 시 개인화 추천 입력값으로 사용한다.
- 데이터 부족 시 최소 설문 응답을 성향 프로필로 변환해 저장한다.
- 기존 성향 프로필을 재사용해 반복 입력 없이 추천 코스를 생성한다.

---

## 3. 점수 규칙

점수형 필드는 모두 `1~5` 범위의 정수로 저장합니다.
| 점수 | 의미 |
| :--- | :--- |
| `1` | 선호도가 매우 낮음 |
| `2` | 선호도가 낮음 |
| `3` | 보통 |
| `4` | 선호도가 높음 |
| `5` | 선호도가 매우 높음 |

---

## 4. Enum 정의

### `sourceType`

| 저장값     | 의미                                  |
| :--------- | :------------------------------------ |
| `survey`   | 최소 설문 기반 성향                   |
| `behavior` | 사용자 행동 데이터 기반 성향          |
| `mixed`    | 설문과 행동 데이터를 함께 반영한 성향 |

### `travelPaceDensity`

| 저장값           | 표시 라벨     |
| :--------------- | :------------ |
| `slow_stay`      | 느긋한 체류형 |
| `balanced`       | 균형형        |
| `dense_schedule` | 빡빡한 일정형 |
| `spontaneous`    | 즉흥형        |
| `long_stay`      | 장기여행형    |

### `spendingTendency`

| 저장값           | 표시 라벨   |
| :--------------- | :---------- |
| `cost_effective` | 가성비형    |
| `moderate`       | 중간 소비형 |
| `luxury`         | 럭셔리형    |

### `companionType`

| 저장값          | 표시 라벨                     |
| :-------------- | :---------------------------- |
| `solo`          | 혼자 여행형                   |
| `couple`        | 연인 여행형                   |
| `friends`       | 친구 여행형                   |
| `family`        | 가족 여행형                   |
| `with_children` | 아이 동반형                   |
| `with_parents`  | 부모님 동반형                 |
| `group`         | 단체 여행형                   |
| `with_pet`      | 반려동물 동반형               |
| `social`        | 새로운 사람과 어울리는 여행형 |

---

## 5. 상세 취향 분류 목록

### 1) 여행 목적 (점수형)

- 휴양형: 쉬고 재충전하는 여행
- 관광형: 유명 명소와 랜드마크 중심
- 문화체험형: 역사, 전통, 현지 문화 중심
- 미식형: 음식점, 시장, 카페 탐방 중심
- 자연탐방형: 산, 바다, 숲, 국립공원 중심
- 액티비티형: 등산, 서핑, 스키, 다이빙 등
- 쇼핑형: 쇼핑몰, 아웃렛, 기념품 중심
- 축제·이벤트형: 공연, 스포츠, 지역 축제 중심
- 웰니스형: 스파, 요가, 명상, 온천 중심
- 자기계발형: 어학, 워케이션, 교육 프로그램 중심

### 2) 여행 속도/일정 밀도 (택1)

- 느긋한 체류형: 한 지역에 오래 머무름
- 균형형: 관광과 휴식을 적절히 배분
- 빡빡한 일정형: 짧은 시간에 많은 장소 방문
- 즉흥형: 현장에서 일정을 결정
- 장기여행형: 몇 주 이상 머무르며 생활하듯 여행

### 3) 여행 장소 취향 (점수형)

- 대도시형
- 소도시·골목형
- 자연·오지형
- 해변·휴양지형
- 산악·고원형
- 역사도시형
- 테마파크·리조트형
- 유명 관광지 선호형
- 숨은 명소 선호형

### 4) 활동 취향 (점수형)

- 관람형: 박물관, 미술관, 공연
- 체험형: 공방, 요리, 전통문화 체험
- 모험형: 익스트림 스포츠, 트레킹
- 사진·영상형
- 미식 탐방형
- 밤문화형
- 쇼핑형
- 휴식형
- 현지인 교류형

### 5) 소비 성향 (택1)

- 가성비형: 가격 대비 만족도 중시
- 중간 소비형
- 럭셔리형: 고급 호텔, 파인다이닝, 전용 서비스

### 6) 동행 형태 (먼저 질문 / 택1)

- 혼자 여행형
- 연인 여행형
- 친구 여행형
- 가족 여행형
- 아이 동반형
- 부모님 동반형
- 단체 여행형
- 반려동물 동반형
- 새로운 사람과 어울리는 여행형

### 7) 음식 취향 (점수형)

- 현지 음식 적극 체험형
- 유명 맛집 중심형
- 길거리 음식형
- 카페·디저트형
- 파인다이닝형
- 익숙한 음식 선호형
- 채식·할랄·알레르기 등 식단 제한형
- 음식보다 관광을 중시하는 유형

### 8) 계절/환경 취향 (택 N)

- `warm_region`: 따뜻한 지역 선호형
- `cold_region`: 추운 지역 선호형
- `summer_resort`: 여름 휴양형
- `winter_sports`: 겨울 스포츠형
- `spring_flower_autumn_foliage`: 봄꽃·가을 단풍형
- `dry_weather`: 건조한 날씨 선호형
- `off_season`: 비수기 여행형
- `peak_season`: 성수기 분위기 선호형

---

## 6. 데이터베이스 컬럼 스펙

| 컬럼                              | 타입        | 역할                                           |
| :-------------------------------- | :---------- | :--------------------------------------------- |
| `id`                              | UUID        | 성향 프로필 PK                                 |
| `user_id`                         | UUID        | 사용자 FK                                      |
| `source_type`                     | TEXT        | 성향 생성 방식 — `survey`, `behavior`, `mixed` |
| `profile`                         | JSONB       | 여행 목적·장소·활동·음식·환경 선호도 전체      |
| `travel_pace_density`             | TEXT        | 일정 밀도 — 목록 필터 및 추천 로직 분기        |
| `spending_tendency`               | TEXT        | 소비 성향 — 예산 추천 기준                     |
| `companion_type`                  | TEXT        | 동행 형태 — 장소/일정 추천 기준                |
| `seasonal_environment_preference` | TEXT[]      | 계절·환경 선호도                               |
| `created_at` / `updated_at`       | TIMESTAMPTZ | 생성·수정 시각                                 |

---

## 7. JSON 예시

```json
{
  "tasteProfileId": "550e8400-e29b-41d4-a716-446655440001",
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "sourceType": "mixed",
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
