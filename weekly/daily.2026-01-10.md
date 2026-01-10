# Daily Idea Planning - 2026-01-10

## 1. Discovery (Ideas)

### 1. **티어 평균 비교 레이더 차트 (Tier Average Comparison Radar)**
- **위치**: Summoner Detail > RoleRadarChart
- **문제**: 현재 레이더 차트는 사용자의 점수만 보여주어, 해당 점수가 실제로 좋은지(상위 몇 %인지, 혹은 평균 이상인지) 직관적으로 알기 어렵습니다.
- **가치**: "골드 티어 평균" 등의 기준선을 함께 표시하여 내 실력의 **상대적 위치**를 명확하게 시각화합니다. 인사이트의 깊이를 더합니다.

### 2. **플레이스타일 태그 "결정적 경기" 연결 (Key Match Highlighter)**
- **위치**: Summoner Detail > Playstyle Tags
- **문제**: "라인전 킬러" 태그가 붙었을 때, 어떤 경기가 이 태그 부여에 가장 큰 영향을 주었는지 알 수 없습니다.
- **가치**: 태그를 클릭하면 해당 성향 점수(예: earlyAggro)가 가장 높았던 매치로 이동하거나 툴팁을 띄워 **설명가능성(Explainability)**을 강화합니다.

### 3. **최근 5경기 vs 전체 추세 비교 (Recent Trend Indicator)**
- **위치**: Summoner Detail > Performance Summary
- **문제**: 전체 평균 점수는 과거의 실력까지 포함되어 현재 폼(Form)을 반영하지 못할 수 있습니다.
- **가치**: "최근 5경기"의 지표를 별도로 계산하여 상승세/하락세를 보여줌으로써 코칭/피드백 가치를 높입니다.

### 4. **AI 분석 "한 줄 액션 아이템" (Actionable One-Liner)**
- **위치**: Summoner Detail > AI Analysis
- **문제**: AI 분석 텍스트가 길어질 경우, 사용자가 당장 무엇을 고쳐야 할지 한눈에 파악하기 어렵습니다.
- **가치**: 분석 결과의 요약을 넘어, "분당 CS를 0.5개 늘리세요"와 같은 **구체적 행동 지침**을 최상단에 강조합니다.

### 5. **Celery 태스크 상태 모니터 (Task Queue Monitor)**
- **위치**: Admin Dashboard
- **문제**: 전적 갱신 요청이 몰릴 때, 백그라운드 워커(Celery)가 정상 작동 중인지 관리자가 UI에서 확인하기 어렵습니다.
- **가치**: 시스템 신뢰성 확보 및 포트폴리오 관점에서 **비동기 인프라 관리 능력**을 보여줄 수 있습니다.

---

## 2. Triage

- **Top 1 Feature**: **티어 평균 비교 레이더 차트 (Tier Average Comparison Radar)**
- **Selection Reason**:
    - **Impact (High)**: 시각적 정보는 텍스트보다 훨씬 빠르게 전달됩니다. 사용자가 자신의 강약점을 "평균"과 비교하며 즉각적인 인사이트를 얻을 수 있습니다.
    - **Confidence (High)**: 현재 `RoleRadarChart` 컴포넌트(`recharts` 사용)에 데이터 시리즈 하나만 추가하면 되므로 구현 난이도가 낮고 효과는 확실합니다.
    - **Ease (High)**: 백엔드에서 복잡한 통계 계산 없이, MVP 단계에서는 하드코딩된 "기준 점수"를 제공하는 것만으로도 충분한 가치를 냅니다.
- **Why others were not selected**:
    - **Key Match**: 백엔드 로직 수정(매치별 기여도 추적)이 다소 복잡할 수 있어 MVP로는 무겁습니다.
    - **Task Monitor**: 관리자용 기능이므로 일반 사용자 경험 개선(Product Value) 우선순위에서 밀립니다.

---

## 3. Spec Draft (Top 1)

### Feature Name
**Role Performance vs Tier Average Visualization**

### Problem Statement
사용자는 자신의 5각형(또는 다각형) 레이더 차트 점수가 "절대적으로 높은지"는 알 수 있지만, "남들보다 잘하는지"는 알 수 없다. 비교군이 부재하여 점수의 해석이 모호하다.

### MVP Scope
- **Backend**: `/api/summoner/{name}/scores` 응답에 `baseline_scores` 필드 추가 (모든 역할군에 대해 고정된 평균값, 예: 50점).
- **Frontend**: `RoleRadarChart` 컴포넌트가 `baseline` 데이터를 받아, 사용자 점수와 겹쳐서 렌더링.
- **UI**: 범례(Legend) 추가 ("My Score", "Tier Average"). 평균선은 회색 점선 등으로 스타일링하여 사용자 데이터와 구분.

### Optional Scope
- 실제 티어별(브론즈/실버/골드 등) 평균 데이터를 DB에서 집계하여 동적으로 제공. (MVP 이후 고려)

### Acceptance Criteria
1. 소환사 상세 페이지의 레이더 차트에 두 개의 다각형이 표시되어야 한다.
2. 하나는 사용자의 점수, 다른 하나는 "평균(Tier Average)" 점수여야 한다.
3. 마우스 오버 시 툴팁에 "내 점수: 70 / 평균: 50"과 같이 비교 수치가 떠야 한다.
4. 백엔드 응답 스키마에 `comparison` 데이터가 포함되어야 한다.

---

## 4. Backlog Draft

### Suggested Issue Title
`[Daily][2026-01-10] Implement Tier Average Comparison in Role Radar Chart`

### Task Breakdown
- **Backend**: `ScoreResponse` Pydantic 모델에 `average_score` 필드 추가 (Default 값 설정).
- **Frontend**: `RoleRadarChart.tsx` 인터페이스 수정 (`averageScores` prop 추가).
- **Frontend**: `Recharts` 설정 업데이트 (`<Radar>` 컴포넌트 추가 렌더링, 색상/스타일 구분).
- **Frontend**: `SummonerDetail.tsx`에서 API 응답의 평균 데이터를 차트 컴포넌트로 전달.

---

## 5. Docs / Notes

### Suggested README Update
- **Screenshots Section**: 레이더 차트 비교 기능 스크린샷 업데이트 ("Now compares your stats against tier averages").

### Questions to Explore
1. "평균"의 기준을 어떻게 잡을 것인가? (현재 DB에 쌓인 전체 유저 평균? 아니면 라이엇 공식 데이터 기반 하드코딩?)
2. `Recharts` 레이더 차트에서 두 영역이 겹칠 때 가시성(Opacity) 처리는 어떻게 하는 것이 가장 직관적인가?
3. 모바일 화면(작은 너비)에서 범례가 차트를 가리지 않도록 하는 레이아웃 전략은?
