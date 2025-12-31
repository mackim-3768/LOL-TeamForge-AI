# Daily Idea Log - 2025-12-31

## 1. Discovery (Ideas)

### 1. AI 분석 컨텍스트 강화 (최근 5경기 트렌드 추가)
- **적용 단계**: AI Analysis
- **문제 해결**: 단순 평균 스탯만으로는 상승세인지 하락세인지, 기복이 심한지 알 수 없음.
- **중요성**: "최근 폼이 좋다/나쁘다"는 LoL 분석에서 매우 중요한 인사이트임. AI 분석의 깊이를 더해줌.

### 2. 점수 로직 시각화 (Radar Chart)
- **적용 단계**: Summoner Detail (Score Calculation 결과 표시)
- **문제 해결**: 사용자는 자신의 점수가 왜 높은지, 낮은지 직관적으로 알기 어려움 (예: KDA는 높은데 시야 점수가 낮아서 종합 점수가 낮은 경우).
- **중요성**: 분석의 '설명력(Explainability)'을 높여주는 핵심 기능. 포트폴리오 시각적 효과가 큼.

### 3. 팀 구성 원클릭 내보내기 (Clipboard Export)
- **적용 단계**: Team Recommendation
- **문제 해결**: 추천받은 팀 구성을 팀원들에게 공유하거나 클라이언트에 입력할 때 불편함.
- **중요성**: 실제 사용자 경험(UX) 편의성을 크게 높여주는 기능.

### 4. 모의 데이터 시나리오 모드 (Mock Scenario Mode)
- **적용 단계**: Summoner Registration / Admin
- **문제 해결**: 개발 및 시연 시 극단적인 케이스(트롤링, 캐리 머신, 서포터형 정글러 등)를 테스트하기 어려움.
- **중요성**: 개발자 경험(DX) 향상 및 포트폴리오 데모 시 다양한 상황 연출 가능.

### 5. AI 페르소나 스위처 (Coach vs Friend vs Analyst)
- **적용 단계**: Admin / User Settings
- **문제 해결**: AI 분석 톤이 일관적이지만 재미가 없음. 사용자가 원하는 스타일(독설가, 친절한 코치 등)로 변경 불가.
- **중요성**: 사용자 맞춤형 경험 제공 및 LLM 활용 능력 과시.

---

## 2. Triage

- **Top 1 Feature**: **점수 로직 시각화 (Radar Chart)**
- **선정 이유**:
  - `recharts` 라이브러리가 이미 프로젝트에 포함되어 있어 구현 비용이 낮음(Feasibility).
  - 숫자로만 나열된 데이터보다 시각적 그래프가 포트폴리오로서의 가치가 훨씬 높음(Impact).
  - 사용자가 자신의 강약점을 한눈에 파악할 수 있어 분석 서비스의 핵심 가치인 '인사이트 제공'에 가장 부합함.
- **탈락 사유 (Others)**:
  - 트렌드 분석: 백엔드 로직 수정이 필요하며 시각적 임팩트가 적음.
  - 내보내기: 편의 기능이지만 핵심 가치는 아님.
  - 시나리오 모드: 내부 개발용 도구에 가까움.
  - 페르소나: 재미 요소지만 분석 신뢰도와는 거리가 있음.

---

## 3. Spec Draft (Top 1)

### Feature Name
**Summoner Stat Radar Chart (소환사 능력치 레이더 차트)**

### Problem Statement
소환사 상세 페이지에서 제공되는 데이터가 텍스트와 숫자로만 구성되어 있어, 해당 소환사의 플레이 스타일(공격적, 안정적, 시야 중심 등)을 한눈에 파악하기 어렵다.

### MVP Scope
- `SummonerDetail` 페이지 상단 또는 요약 섹션에 Radar Chart 추가.
- 5가지 축(Axis) 사용:
  1. **전투 (Combat)**: KDA, Kill 관여율 기반
  2. **성장 (Farming)**: CS/min, Gold/min 기반
  3. **시야 (Vision)**: Vision Score/min 기반
  4. **생존 (Survival)**: Death/min (역수) 기반
  5. **딜량 (Damage)**: DPM (Damage Per Minute) 기반
- 각 축은 0~100점 척도로 정규화하여 표시.
- 마우스 오버 시 실제 수치 툴팁 제공.

### Optional Scope
- 티어 평균(예: 골드 티어 평균)과 겹쳐서 비교 보여주기.
- 최근 20게임 vs 전체 시즌 비교.

### Acceptance Criteria
- [ ] `SummonerDetail` 페이지 진입 시 레이더 차트가 렌더링되어야 한다.
- [ ] 5개 축(전투, 성장, 시야, 생존, 딜량)이 모두 표시되어야 한다.
- [ ] 데이터가 없는 경우(0게임) 빈 차트나 안내 메시지를 보여주어야 한다.
- [ ] 차트 데이터는 백엔드 `MatchPerformance` 데이터를 기반으로 계산되거나 API로 전달받아야 한다.

---

## 4. Backlog Draft

### GitHub Issue Title
`[Daily][2025-12-31] feat: Add Radar Chart for Summoner Stats visualization`

### Task Breakdown

#### Frontend
- [ ] `recharts`를 활용한 `StatRadarChart` 컴포넌트 생성.
- [ ] `SummonerDetail` 페이지 레이아웃 수정 (차트 영역 확보).
- [ ] API 응답 데이터(매치 리스트)를 차트용 데이터 포맷(5개 축 점수)으로 변환하는 유틸리티 함수 구현.
- [ ] 반응형 디자인 적용 (모바일 대응).

#### Backend
- [ ] (필요 시) `/summoners/{name}` 엔드포인트 응답에 집계된 통계 데이터가 포함되어 있는지 확인 및 보완.
- [ ] (Optional) 백엔드 단에서 정규화된 점수(0~100) 계산 로직 추가 (프론트엔드 연산 부담 경감).

---

## 5. Docs / Notes

### Suggested README Update
- **Screenshots Section**: 레이더 차트가 적용된 소환사 상세 페이지 스크린샷 추가.
- **Features List**: "Interactive Data Visualization (Radar Chart)" 항목 추가.

### Questions for Next Cycle
1. 레이더 차트의 최대값(100점 기준)을 어떻게 설정할 것인가? (예: 챌린저 평균? 아니면 해당 티어 내 상위 1%?)
2. 서포터 포지션의 경우 CS나 DPM이 낮을 수밖에 없는데, 포지션별 보정을 어떻게 적용할 것인가?
3. 모바일 화면에서 차트의 가독성을 어떻게 유지할 것인가?
