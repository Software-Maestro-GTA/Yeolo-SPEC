# Yeolo-SPEC (여로 명세서 저장소)

제로터치 초개인화 여행 플랫폼 **여로(Yeolo)**의 공식 요구사항, 기능 명세, 도메인 정의 및 API 규격 문서를 통합 관리하는 저장소입니다.

---

## 📂 프로젝트 폴더 구조

```bash
Yeolo-SPEC/
├── README.md                 # 본 문서 (프로젝트 개요 및 구조 설명)
├── requirement-specs/        # [요구사항] 요구사항 정의서 디렉토리
│   ├── requirement.md        # 요구사항 정의서 종합 목록 (인덱스)
│   └── REQ-*.md              # 요구사항 개별 세부 명세서 (REQ-1 ~ REQ-12)
├── functional-specs/         # [기능명세] 기능 명세서 디렉토리
│   ├── functional.md         # 기능 명세서 종합 목록 (인덱스)
│   └── FUN-*.md              # 기능별 비즈니스 로직 및 예외 처리 세부 명세서 (FUN-1 ~ FUN-7)
├── domain-specs/             # [도메인] 데이터 및 도메인 정의서 디렉토리
│   ├── domain.md             # 도메인 정의서 종합 목록 (인덱스)
│   └── DOM-*.md              # 핵심 도메인별 데이터 구조 및 컬럼 스펙 명세서 (DOM-1 ~ DOM-5)
├── api-specs/                # [API 규격] API 명세서 디렉토리
│   ├── api.md                # API 명세서 종합 목록 (인덱스)
│   └── API-*.md              # FE-BE 및 BE-AI 내부 API 규격서 (API-FB-1 ~ API-BA-6)
└── design-specs/             # [디자인] UI/UX 디자인 명세서 디렉토리
    ├── design.md             # 디자인 명세서 종합 목록 (인덱스)
    └── DES-*.md              # 개별 컴포넌트 디자인 상세 명세서 (DES-1 ~)
```

---

## 📝 디렉토리별 세부 설명

### 1. [요구사항 정의서](./requirement-specs/requirement.md) (`requirement-specs/`)

- **역할**: 플랫폼의 핵심 비즈니스 요구사항 및 기능적/비기능적 기획 요소를 정의합니다.
- **구성**: [requirement.md](./requirement-specs/requirement.md) 인덱스 파일과 요구사항 정의서([REQ-\*.md](./requirement-specs/))들로 구성되어 있으며, 각 요구사항별 구체적인 설명 및 **인수 기준(Acceptance Criteria)**을 포함합니다.

### 2. [기능 명세서](./functional-specs/functional.md) (`functional-specs/`)

- **역할**: 요구사항이 시스템 상에서 어떻게 동작하는지 개발 관점의 세부 스펙으로 풀어서 명시합니다.
- **구성**: [functional.md](./functional-specs/functional.md) 인덱스 파일과 기능 명세서([FUN-\*.md](./functional-specs/))로 구성되며, 비즈니스 정책, 세부 파이프라인 및 상황별 **예외 처리(Exception Handling)**가 명세되어 있습니다.

### 3. [데이터 및 도메인 정의서](./domain-specs/domain.md) (`domain-specs/`)

- **역할**: 플랫폼 내부에서 관리 및 유지되어야 하는 영속성 데이터 모델의 스펙과 제약 사항을 정의합니다.
- **구성**: [domain.md](./domain-specs/domain.md) 인덱스 파일과 도메인 규격서([DOM-\*.md](./domain-specs/))로 구성되어 있습니다. 데이터베이스 테이블 컬럼 스펙, 허용되는 Enum 값의 표시 라벨 및 입출력 JSON 구조 예시를 포함합니다.

### 4. [API 명세서](./api-specs/api.md) (`api-specs/`)

- **역할**: 클라이언트-서버(FE-BE) 및 내부 AI 엔진(BE-AI) 간의 데이터 전송 방식 및 통신 스펙을 정의합니다.
- **구성**: [api.md](./api-specs/api.md) 인덱스 파일과 API 호출 규격서([API-\*.md](./api-specs/))로 구성됩니다. REST 및 SSE 통신 방식, Request Body 구조, 성공 응답 사양(Status 200 / Stream JSON), 그리고 실패 상황별 에러 상태 코드와 응답 메시지가 상세히 기술되어 있습니다.

### 5. [디자인 명세서](./design-specs/design.md) (`design-specs/`)

- **역할**: 플랫폼 화면 및 UI 컴포넌트의 레이아웃, CSS/StyleSheet 테마 토큰 및 마크업 설계를 정의합니다.
- **구성**: [design.md](./design-specs/design.md) 인덱스 파일과 디자인 상세 규격서([DES-\*.md](./design-specs/))로 구성됩니다. 컴포넌트 HTML 마크업 계층 구조, 패딩/마진/폰트 스케일 및 다크/라이트 테마별 변수 매핑이 상세히 기술되어 있습니다.
