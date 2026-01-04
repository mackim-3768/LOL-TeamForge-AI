# [Daily] 2026-01-04 아이디어 노트

## 1. Discovery (Ideas)

| # | 아이디어명 | 적용 단계 | 문제 정의 (Problem) | 중요성 (Why) |
|---|---|---|---|---|
| 1 | **최근 퍼포먼스 트렌드 그래프** | 소환사 상세 (SummonerDetail) | 매치 목록의 숫자만으로는 최근 실력의 등락이나 기복을 한눈에 파악하기 어려움. | 사용자의 성장/하락세를 시각적으로 보여주어 **인사이트 깊이**를 강화함. |
| 2 | **매치 타임라인 요약 시각화** | 매치 상세 (MatchDetail) | 게임 승패의 결정적 순간(예: 바론 스틸, 한타)을 파악하려면 전체 리플레이를 봐야 함. | 게임의 흐름을 빠르게 파악할 수 있어 **설명 가능성(Explainability)**을 높임. |
| 3 | **AI 분석 근거(Reasoning) 상세화** | AI 분석 (Analysis) | AI가 왜 그런 추천을 했는지에 대한 구체적인 수치적 근거(Feature attribution)가 부족함. | "왜"를 설명함으로써 AI 결과에 대한 **신뢰도**와 **설명 가능성**을 높임. |
| 4 | **라인전 상대와의 지표 비교 (Laning Phase Diff)** | 매치 상세 (MatchDetail) | 라인전 단계에서의 유불리(15분 골드/CS 차이 등)를 명확히 비교하기 어려움. | 초반 스노우볼링 능력을 객관적으로 평가하여 **비교/분석 깊이**를 더함. |
| 5 | **챔피언 숙련도 기반 큐레이션** | 팀 구성 추천 (TeamBuilder) | 단순히 조합 점수가 높은 챔피언을 추천하지만, 유저가 못 다루는 챔피언일 수 있음. | 현실적인 추천을 통해 **사용자 경험(UX)**과 추천의 **실효성**을 높임. |

---

## 2. Triage

### **Top 1 Feature: 최근 퍼포먼스 트렌드 그래프**

**선정 이유:**
- **가시성(Visibility):** 텍스트/표 위주의 현재 상세 페이지에 강력한 시각적 요소를 더해 UX를 크게 개선합니다.
- **구현 용이성(Feasibility):** 이미 프론트엔드에 `recharts` 라이브러리가 설치되어 있고, 필요한 데이터(`kda`, `damage`, `gold` 등)가 `SummonerDetail` 페이지에 이미 로드(`matches` state)되어 있어 백엔드 수정 없이 즉시 구현 가능합니다.
- **포트폴리오 가치:** 데이터 시각화 역량을 잘 보여줄 수 있는 기능입니다.

**미선정 이유:**
- **매치 타임라인:** 타임라인 데이터(Event data)를 Riot API에서 추가로 파싱하고 저장하는 백엔드 작업이 선행되어야 함.
- **AI 근거 상세화:** AI 프롬프트 엔지니어링 및 모델 응답 구조 변경이 필요하여 공수가 큼.
- **라인전 비교:** 상대 라이너 데이터를 매칭하는 로직이 추가로 필요함.
- **챔피언 숙련도:** 숙련도 데이터 수집 API 연동이 추가로 필요함.

---

## 3. Spec Draft (Top 1)

### Feature Name
**최근 20게임 퍼포먼스 트렌드 (Recent Performance Trend)**

### Problem Statement
사용자는 자신의 최근 전적 목록(리스트)을 보며 "내가 최근에 잘하고 있는가?"를 직관적으로 판단하기 어렵습니다. 수치의 변화 추이를 그래프로 제공하여 이를 해결합니다.

### MVP Scope
- **위치:** `SummonerDetail` 페이지의 매치 리스트 상단.
- **데이터:** 현재 로드된 최근 20게임(`matches`) 데이터 활용.
- **기능:**
  - X축: 최근 게임 순서 (최신순).
  - Y축: 선택된 지표 (기본값: KDA).
  - 메트릭 토글 버튼: KDA, 데미지(DPM), 골드(GPM), CS(CPM) 중 선택 가능.
  - 그래프에 승/패 여부를 색상(점)으로 표시 (승: 파랑, 패: 빨강).

### Optional Scope
- 특정 챔피언이나 포지션만 필터링하여 그래프 다시 그리기.
- 평균선(Average Line) 추가.

### Acceptance Criteria
1. 소환사 상세 페이지 진입 시 매치 리스트 위에 라인 차트가 표시되어야 한다.
2. 차트의 데이터 포인트는 아래 매치 리스트와 일치해야 한다.
3. KDA, DPM, GPM, CS 버튼을 누르면 차트의 Y축 데이터가 즉시 변경되어야 한다.
4. 데이터 포인트에 마우스를 올리면 해당 게임의 상세 수치 툴팁이 나와야 한다.

---

## 4. Backlog Draft

### **[Daily][2026-01-04] 최근 퍼포먼스 트렌드 그래프 추가**

#### Frontend
- [ ] `MatchTrendChart.tsx` 컴포넌트 생성 (`recharts` 활용).
  - Props: `matches: MatchPerformance[]`
- [ ] 차트 내 메트릭 선택 UI (Toggle Group/Button) 구현.
- [ ] `SummonerDetail.tsx`에 `MatchTrendChart` 컴포넌트 배치 (매치 리스트 상단).
- [ ] 모바일 반응형 대응 (그래프 크기 자동 조절).

#### Backend
- (없음 - 기존 API 활용)

#### Docs
- (없음)

---

## 5. Docs / Notes

### Suggested README Update
- (없음 - 기능 구현 후 스크린샷 추가 고려)

### Questions & Uncertainties
1. `MatchPerformance` 데이터에 `dpm` 필드가 `total_damage`로만 되어 있는데, `game_duration` 정보가 리스트 API(`getMatches`)에 포함되어 있는지 확인 필요. (현재 `MatchPerformance` 타입에는 `game_creation`만 있고 `duration`이 없음. DPM 계산을 위해 `duration`이 필요한지, 아니면 그냥 `Total Damage`로 보여줄지 결정 필요. -> 일단 `Total Damage`로 진행하거나 백엔드 `MatchListResponse` 수정 검토.)
2. `ScoreResponse`에 있는 역할군별 점수(`score`)를 매치별로도 산출해서 그래프로 보여줄 수 있다면 더 좋을 것 같음. (추후 고도화)
