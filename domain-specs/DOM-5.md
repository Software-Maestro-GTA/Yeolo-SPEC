# [DOM-5] 이미지 메타데이터 전처리 정보 (Image Metadata Preprocessing)

사용자 동의를 받은 뒤, 클라이언트가 각 사진의 촬영 좌표와 촬영 시간을 서버로 전송합니다. 서버는 좌표를 Reverse Geocode로 변환해 위치 정보를 전처리하고, AI 서버는 전달받은 전처리 데이터를 재가공해 LLM에 사용자 여행 성향 추출을 질의합니다.
이미지 내용 자체를 분석하거나 사람이 태그를 직접 입력하는 방식이 아니라, **사진이 찍힌 위치와 시간의 패턴**을 바탕으로 사용자의 여행 성향을 추론합니다.

---

## 1. 주요 필드 정의

- `imageMetadataId`: 이미지 메타데이터 고유 식별자 (UUID)
- `userId`: 사용자 고유 식별자 (UUID)
- `sourceImageId`: 클라이언트에서 부여한 이미지 식별자
- `capturedAt`: 포맷팅된 이미지 촬영 시각
- `latitude`: 이미지 촬영 위도
- `longitude`: 이미지 촬영 경도
- `location`: 서버에서 Reverse Geocode로 추출한 위치 정보
- `timeContext`: 클라이언트/서버에서 계산한 시간 맥락 정보
- `placeContext`: 장소 유형 및 방문 맥락 정보
- `createdAt`: 메타데이터 생성 시각

---

## 2. 전처리 및 AI 파이프라인

1. **Client** — 사용자 동의 후 서버로 여행 사진의 좌표와 포매팅된 시간 값을 전송한다.
2. **Server** — 좌표 값을 바탕으로 Reverse Geocode를 진행해서 위치 정보를 전처리한다.
3. **Server** — 전처리된 위치·시간 정보를 AI 서버로 전송한다.
4. **AI** — 전송된 정보를 바탕으로 데이터를 재가공한 뒤 LLM에 사용자 성향 추출을 질의한다.

---

## 3. 전송 및 처리 원칙

- 좌표와 시간 정보는 사용자 동의 후에만 서버로 전송한다.
- 서버는 원본 이미지를 저장하지 않고, 분석에 필요한 메타데이터만 저장한다.
- 클라이언트는 촬영 시간을 ISO 8601 형식으로 포맷팅해 서버로 전송한다.
- 서버는 좌표를 Reverse Geocode하여 위치 정보를 추출한다.
- AI 서버에는 원본 이미지가 아니라 위치·시간 기반 전처리 정보를 전달한다.

---

## 4. 데이터 흐름별 상세 필드

### 1) Client에서 추출할 정보

| 필드                                   | 타입        | 역할                                                               |
| :------------------------------------- | :---------- | :----------------------------------------------------------------- |
| `sourceImageId`                        | TEXT        | 클라이언트에서 부여한 이미지 식별자                                |
| `capturedAt`                           | TIMESTAMPTZ | EXIF 기준 이미지 촬영 시각을 ISO 8601 형식으로 포맷팅한 값         |
| `capturedDate`                         | DATE        | 촬영 날짜                                                          |
| `capturedTime`                         | TIME        | 촬영 시간                                                          |
| `latitude`                             | DOUBLE      | 이미지 촬영 위도                                                   |
| `longitude`                            | DOUBLE      | 이미지 촬영 경도                                                   |
| `currentLatitude` / `currentLongitude` | DOUBLE      | 여행 이미지 추출 기준이 되는 사용자 현재 위치                      |
| `timezone`                             | TEXT        | 촬영 시간 포맷팅에 사용한 타임존 (사용자 설정 또는 좌표 기반 추정) |

### 2) Client에서 Server로 전송할 정보

| 필드                     | 타입        | 역할                               |
| :----------------------- | :---------- | :--------------------------------- |
| `userId`                 | UUID        | 사용자 식별자                      |
| `sourceImageId`          | TEXT        | 클라이언트 이미지 식별자           |
| `capturedAt`             | TIMESTAMPTZ | 포맷팅된 촬영 시각                 |
| `latitude` / `longitude` | DOUBLE      | Reverse Geocode에 사용할 촬영 좌표 |
| `timezone`               | TEXT        | 촬영 시간 해석에 사용할 타임존     |

### 3) Server에서 Reverse Geocode로 추출할 위치 정보

| 필드         | 타입   | 역할                                                                                 |
| :----------- | :----- | :----------------------------------------------------------------------------------- |
| `country`    | TEXT   | 촬영 국가                                                                            |
| `city`       | TEXT   | 촬영 도시                                                                            |
| `region`     | TEXT   | 촬영 지역 또는 광역 행정구역                                                         |
| `district`   | TEXT   | 구/군/동 등 세부 행정구역                                                            |
| `placeName`  | TEXT   | 좌표와 가장 가까운 장소명                                                            |
| `placeTypes` | TEXT[] | 장소 유형 — `tourist_attraction`, `museum`, `cafe`, `restaurant`, `park`, `beach` 등 |

### 4) Server에서 추출할 시간 맥락 정보

| 필드         | 타입    | 역할                                                             |
| :----------- | :------ | :--------------------------------------------------------------- |
| `dayOfWeek`  | TEXT    | 촬영 요일 — `mon`, `tue`, `wed`, `thu`, `fri`, `sat`, `sun`      |
| `isWeekend`  | BOOLEAN | 주말 촬영 여부                                                   |
| `timeBucket` | TEXT    | 촬영 시간대 — `dawn`, `morning`, `afternoon`, `evening`, `night` |
| `season`     | TEXT    | 촬영 계절 — `spring`, `summer`, `autumn`, `winter`               |

### 5) Server에서 AI 서버로 전송할 정보

| 필드                  | 타입    | 역할                                                         |
| :-------------------- | :------ | :----------------------------------------------------------- |
| `userId`              | UUID    | 사용자 식별자                                                |
| `items`               | JSONB[] | 사진별 위치 정보와 시간 맥락 정보 목록                       |
| `items.sourceImageId` | TEXT    | 사진별 식별자                                                |
| `items.location`      | JSONB   | Reverse Geocode로 추출한 국가, 도시, 지역, 장소명, 장소 유형 |
| `items.timeContext`   | JSONB   | 촬영 요일, 주말 여부, 시간대, 계절                           |

---

## 5. Enum 정의

### `timeBucket` 시간대 구분

| 저장값      | 시간 범위   | 분석 의미              |
| :---------- | :---------- | :--------------------- |
| `dawn`      | 05:00 이전  | 새벽 이동/촬영 가능성  |
| `morning`   | 05:00~11:59 | 오전 활동 선호         |
| `afternoon` | 12:00~16:59 | 낮 시간 활동           |
| `evening`   | 17:00~20:59 | 저녁 일정/야경 전 활동 |
| `night`     | 21:00 이후  | 야간 활동 가능성       |

### `season` 계절 구분

| 저장값   | 기준   | 분석 의미                       |
| :------- | :----- | :------------------------------ |
| `spring` | 3~5월  | 봄꽃/온화한 날씨 선호 신호      |
| `summer` | 6~8월  | 여름 휴양/해변 선호 신호        |
| `autumn` | 9~11월 | 단풍/선선한 날씨 선호 신호      |
| `winter` | 12~2월 | 겨울 여행/겨울 스포츠 선호 신호 |

---

## 6. 데이터베이스 컬럼 스펙

| 컬럼                                       | 타입        | 역할                                 |
| :----------------------------------------- | :---------- | :----------------------------------- |
| `id`                                       | UUID        | 이미지 메타데이터 PK                 |
| `user_id`                                  | UUID        | 사용자 FK                            |
| `source_image_id`                          | TEXT        | 클라이언트 이미지 식별자             |
| `captured_at`                              | TIMESTAMPTZ | 포맷팅된 촬영 시각                   |
| `captured_date` / `captured_time`          | DATE / TIME | 촬영 날짜와 시간                     |
| `latitude` / `longitude`                   | DOUBLE      | 사용자 동의 기반 촬영 좌표           |
| `timezone`                                 | TEXT        | 촬영 시간 해석에 사용한 타임존       |
| `country` / `city` / `region` / `district` | TEXT        | Reverse Geocode 결과 위치 정보       |
| `place_name`                               | TEXT        | 추정 장소명                          |
| `place_id`                                 | TEXT        | 장소 식별자                          |
| `place_types`                              | TEXT[]      | 장소 유형                            |
| `time_context`                             | JSONB       | 요일, 시간대, 계절 등 시간 파생 정보 |
| `created_at` / `updated_at`                | TIMESTAMPTZ | 생성·수정 시각                       |

---

## 7. JSON 예시

### 1) Client -> Server 전송 JSON

```json
{
  "images": [
    {
      "sourceImageId": "local-image-001",
      "capturedAt": "2026-07-14T10:00:00+09:00",
      "latitude": 33.4589,
      "longitude": 126.9422,
      "timezone": "Asia/Seoul"
    }
  ]
}
```

### 2) Server -> AI 서버 전송 전처리 JSON

```json
{
  "items": [
    {
      "sourceImageId": "local-image-001",
      "location": {
        "country": "대한민국",
        "city": "제주",
        "region": "서귀포",
        "district": "성산읍",
        "placeName": "성산일출봉",
        "placeTypes": ["tourist_attraction", "natural_feature"]
      },
      "timeContext": {
        "capturedAt": "2026-07-14T10:00:00+09:00",
        "dayOfWeek": "tue",
        "isWeekend": false,
        "timeBucket": "morning",
        "season": "summer"
      }
    },
    {
      "sourceImageId": "local-image-002",
      "location": {
        "country": "대한민국",
        "city": "제주",
        "region": "서귀포",
        "district": "성산읍",
        "placeName": "카페",
        "placeTypes": ["cafe", "food"]
      },
      "timeContext": {
        "capturedAt": "2026-07-14T14:20:00+09:00",
        "dayOfWeek": "tue",
        "isWeekend": false,
        "timeBucket": "afternoon",
        "season": "summer"
      }
    },
    {
      "sourceImageId": "local-image-003",
      "location": {
        "country": "대한민국",
        "city": "제주",
        "region": "서귀포",
        "district": "안덕면",
        "placeName": "해변",
        "placeTypes": ["beach", "natural_feature"]
      },
      "timeContext": {
        "capturedAt": "2026-07-14T18:30:00+09:00",
        "dayOfWeek": "tue",
        "isWeekend": false,
        "timeBucket": "evening",
        "season": "summer"
      }
    }
  ]
}
```
