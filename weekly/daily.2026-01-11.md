# Daily Feature Planning - 2026-01-11

## 1. Discovery (Ideas)

### 1. 플레이스타일 태그 설명 툴팁 (Tag Explanation Tooltip)
- **적용 위치:** 소환사 상세 페이지 > 플레이스타일 태그 리스트
- **해결 문제:** 사용자는 "섬 파밍형 탑" 같은 태그를 보고, 이것이 CS 수급 때문인지 합류 저조 때문인지 구체적인 데이터 근거를 알기 어렵습니다.
- **중요성:** 분석 결과의 **설명 가능성(Explainability)**을 강화하여, 서비스 신뢰도를 높이고 사용자에게 명확한 피드백을 제공합니다.

### 2. 프로 선수/아키타입 유사도 비교 (Pro Archetype Comparison)
- **적용 위치:** 분석 리포트 하단
- **해결 문제:** 추상적인 점수(예: 전투 7.5점)만으로는 사용자가 자신의 수준이나 스타일을 직관적으로 파악하기 어렵습니다.
- **중요성:** "페이커와 85% 유사한 플레이스타일"과 같은 문구는 높은 흥미와 공유 욕구를 유발하여 바이럴 효과를 기대할 수 있습니다.

### 3. 약점 및 나쁜 습관 탐지기 (Bad Habit Detector)
- **적용 위치:** 분석 요약 섹션
- **해결 문제:** 현재 시스템은 긍정적인 태그 위주이나, 사용자는 실력 향상을 위해 고쳐야 할 구체적인 약점(예: "시야 점수 하위 10%")을 알고 싶어 합니다.
- **중요성:** 단순 분석을 넘어 실질적인 **Actionable Insight**를 제공하여 교육적 가치를 더합니다.

### 4. 최근 20게임 지표 변화 그래프 (Metric Trend Graph)
- **적용 위치:** 소환사 상세 페이지 > 통계 탭
- **해결 문제:** 리스트 형태의 전적은 최근 폼의 상승/하락 추세를 한눈에 파악하기 어렵습니다.
- **중요성:** 시각적 데이터를 통해 사용자에게 성장 경험을 제공하고 페이지 체류 시간을 증대시킵니다.

### 5. 점수 산출 디버그 모드 (Score Calculation Debug Mode)
- **적용 위치:** 어드민 페이지 또는 URL 파라미터 활성화
- **해결 문제:** 개발자나 헤비 유저는 점수가 어떻게 산출되었는지(Raw Data -> Normalized Score) 검증하고 싶어 합니다.
- **중요성:** **DX(Developer Experience)** 개선 및 알고리즘의 투명성을 확보하여 커뮤니티의 검증을 유도할 수 있습니다.

---

## 2. Triage

- **Selected:** **플레이스타일 태그 설명 툴팁**
- **Reasoning (ICE):**
  - **Impact (High):** 사용자가 가장 먼저 보는 결과물인 '태그'의 설득력을 높여 핵심 경험을 개선합니다. (Priority #2: Analysis transparency)
  - **Confidence (High):** 이미 백엔드에 가중치(`weights`) 데이터가 존재하므로, 이를 노출하기만 하면 됩니다.
  - **Ease (High):** 복잡한 로직 변경 없이 API 응답 필드 추가와 프론트엔드 툴팁 적용으로 구현 가능합니다.
- **Rejection Notes:**
  - **프로 비교:** 프로 선수의 기준 데이터(Archetype) 구축 선행이 필요합니다.
  - **약점 탐지:** 부정적 피드백에 대한 UI/UX 톤앤매너 설계가 선행되어야 합니다.
  - **그래프:** 차트 라이브러리 도입 등 프론트엔드 공수가 큽니다.

---

## 3. Spec Draft

### Feature Name
**태그 결정 원인 분석 (Tag Reasoning Breakdown)**

### Problem Statement
사용자는 자동 부여된 플레이스타일 태그의 구체적인 근거를 알 수 없어, 분석 결과에 대해 의문을 가지거나 막연하게 받아들입니다.

### MVP Scope
- **Backend:** `SummonerPlaystyleTag` 응답 시, 해당 태그 점수에 기여한 상위 3개 차원(Dimension)과 기여도를 포함하여 반환합니다.
- **Frontend:** 태그 칩(Chip)에 마우스 호버 시, 툴팁(Tooltip)을 띄워 결정적인 요인들을 텍스트로 표시합니다. (예: "높은 초반 교전, 낮은 리스크 감수")

### Optional Scope
- 각 팩터별 기여도를 미니 프로그레스 바(Bar) 형태로 시각화.
- 긍정적 요인뿐만 아니라 태그 획득을 방해한 부정적 요인 표시.

### Acceptance Criteria
1. API는 각 태그별로 `reasoning` 리스트(팩터 이름, 기여도)를 반환해야 한다.
2. 프론트엔드 `SummonerDetail` 페이지에서 태그에 마우스를 올리면 툴팁이 0.5초 이내에 나타나야 한다.
3. 툴팁에는 최소 1개 이상의 결정적 요인이 한국어 라벨로 표시되어야 한다.

---

## 4. Backlog Draft

### Suggested Title
`[Daily][2026-01-11] 플레이스타일 태그 근거(Reasoning) 노출 기능 구현`

### Task Breakdown
1. **[Backend]** `TagDefinition` 및 `evaluate_tags_for_role` 로직 수정
   - 태그 선정 시 계산된 점수(`score`)와 각 가중치 항목의 기여도를 추적하여 반환 구조체에 포함.
2. **[Backend]** API Response Schema 업데이트
   - `SummonerPlaystyleTag` 모델에 `reasoning: List[str]` 또는 상세 객체 추가.
3. **[Frontend]** `TagTooltip` 컴포넌트 구현
   - MUI `Tooltip`을 활용하여 태그 근거 데이터를 표시하는 래퍼 컴포넌트 생성.
4. **[Frontend]** `SummonerDetail` 페이지 연동
   - API로부터 받은 `reasoning` 데이터를 툴팁에 바인딩.

---

## 5. Docs / Notes

### README Update Recommendation
- `## Features` 섹션에 **"Transparent Metrics (투명한 분석 지표)"** 항목을 추가하여, AI/알고리즘이 '블랙박스'가 아님을 강조하십시오.

### Questions to Explore
1. 가중치가 음수인 항목(예: Risk가 낮아야 부여되는 태그)은 사용자에게 어떻게 표현하는 것이 직관적인가? ("안정적인 플레이" vs "낮은 데스")
2. 모바일 터치 환경에서 툴팁 UX는 어떻게 처리할 것인가? (클릭 시 하단 시트 등)
3. 향후 다국어 지원 시, 팩터 이름("초반 교전" 등)의 관리 포인트는 어디에 둘 것인가?
