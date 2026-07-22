# [DOM-2] 코스 정보 (Course Recommendation)

개인 여행 성향과 여행 조건을 바탕으로 생성된 추천 코스를 저장하는 도메인입니다. 추천 결과는 사용자별로 저장되며, 어떤 성향 프로필과 요청 조건을 바탕으로 생성되었는지 추적할 수 있어야 합니다.

---

## 1. 주요 필드 정의

- `courseId`: 코스 고유 식별자 (UUID)
- `userId`: 코스 소유자 (UUID)
- `title`: 코스 제목 (예: "2박 3일 서귀포 감성 가득 힐링 코스")
- `destinationCountry`: 여행 국가
- `destinationCity`: 여행 도시
- `startDate`: 여행 시작일
- `totalDays`: 총 여행 일수
- `tags`: 코스 태그
- `recommendationReason`: 추천 이유
- `constraints`: 코스 생성 시 반영한 제약 조건
- `itinerary`: 일자·방문지·순서 전체

---

## 2. 저장 목적

- AI가 생성한 여행 코스를 사용자별로 저장한다.
- 여행 국가·도시, 시작일, 여행 일수 등 코스 표시와 조회에 필요한 기본 정보를 저장한다.
- 추천 결과의 추천 이유, 적용 제약 조건을 함께 저장해 사용자가 코스를 이해할 수 있게 한다.
- 일자별 방문지·순서·시간·이동 정보는 `itinerary`에 저장해 코스 상세 화면에서 활용한다.

---

## 3. Enum 및 제약 정의

### `constraints` 제약 조건 구조

| 필드                     | 타입    | 역할                                                     |
| :----------------------- | :------ | :------------------------------------------------------- |
| `budgetType`             | TEXT    | 예산 성향 — `cost_effective`, `standard`, `luxury`       |
| `maxTravelMinutesPerDay` | INTEGER | 하루 최대 이동 시간                                      |
| `preferredTransport`     | TEXT[]  | 선호 이동 수단 — `walking`, `transit`, `driving`, `taxi` |
| `pace`                   | TEXT    | 일정 밀도 — `relaxed`, `balanced`, `dense`               |
| `mustIncludeCategories`  | TEXT[]  | 반드시 포함할 장소 카테고리                              |
| `avoidCategories`        | TEXT[]  | 제외할 장소 카테고리                                     |

### `transportToNext` 이동 방법

| 저장값    | 의미           |
| :-------- | :------------- |
| `walking` | 도보 이동      |
| `transit` | 대중교통 이동  |
| `driving` | 자동차 이동    |
| `taxi`    | 택시 이동      |
| `none`    | 다음 장소 없음 |

---

## 4. Itinerary 상세 구조

- `days`
  - `day`: 1일 차, 2일 차 등 (INTEGER)
  - `date`: 해당 일자의 날짜 (DATE 포맷)
  - `memo`: 일자별 메모 (TEXT)
  - `stops`
    - `sequence`: 해당 일자의 방문 순서 (INTEGER)
    - `placeId`: Google Maps Place ID (TEXT)
    - `placeName`: 장소명 (TEXT)
    - `category`: 장소 분류 (식당, 카페, 관광지, 숙소 등)
    - `arrivalTime`: 도착 시간 (HH:mm)
    - `stayMinutes`: 머무는 시간 (INTEGER)
    - `memo`: 장소별 메모
    - `transportToNext`: 다음 장소까지 이동 방법 (Enum)
    - `travelMinutesToNext`: 다음 장소까지 예상 이동 시간 (INTEGER)
    - `cost`: 예상 비용 (INTEGER)
    - `reason`: 해당 장소를 추천한 이유 (TEXT)

---

## 5. 데이터베이스 컬럼 스펙

| 컬럼                        | 타입        | 역할                                   |
| :-------------------------- | :---------- | :------------------------------------- |
| `id`                        | UUID        | 코스 PK                                |
| `user_id`                   | UUID        | 소유자 FK                              |
| `title`                     | TEXT        | 코스 제목                              |
| `destination_country`       | TEXT        | 여행 국가                              |
| `destination_city`          | TEXT        | 여행 도시                              |
| `total_days`                | SMALLINT    | 총 일수 — 필터·정렬용                  |
| `start_date`                | DATE        | 시작일                                 |
| `tags`                      | TEXT[]      | 태그 — 필터용                          |
| `recommendation_reason`     | TEXT        | AI 추천 요약 이유                      |
| `constraints`               | JSONB       | 이동 시간, 예산, 영업시간 등 적용 제약 |
| `itinerary`                 | JSONB       | 일자·방문지·순서 전체                  |
| `created_at` / `updated_at` | TIMESTAMPTZ | 생성·수정 시각                         |

---

## 6. JSON 예시

```json
{
  "courseId": "550e8400-e29b-41d4-a716-446655440030",
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "title": "2박 3일 서귀포 감성 가득 힐링 코스",
  "destinationCountry": "대한민국",
  "destinationCity": "제주",
  "startDate": "2026-08-01",
  "totalDays": 3,
  "tags": ["힐링", "카페", "자연"],
  "recommendationReason": "카페·자연·여유로운 일정 선호도가 높아 이동 거리가 짧고 체류 시간이 긴 코스로 구성했습니다.",
  "itinerary": {
    "days": [
      {
        "day": 1,
        "date": "2026-08-01",
        "memo": "도심 위주로 가볍게",
        "stops": [
          {
            "sequence": 1,
            "placeId": "ChIJN1t_tDeuEmsRUsoyG83frY4",
            "placeName": "함덕 해수욕장",
            "category": "beach",
            "arrivalTime": "10:00",
            "stayMinutes": 90,
            "memo": "오픈런 추천",
            "transportToNext": "transit",
            "travelMinutesToNext": 35,
            "cost": 0,
            "reason": "해변·휴양지 선호도가 높아 첫 일정으로 추천"
          }
        ]
      }
    ]
  }
}
```
