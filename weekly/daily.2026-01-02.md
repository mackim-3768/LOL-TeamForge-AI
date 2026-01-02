# Daily Idea Log (2026-01-02)

## 1. Discovery (Ideas)

### 1. 매치 상세 - 라인 상대 비교 (Head-to-Head)
- **적용 위치**: `SummonerDetail` 페이지의 매치 상세 모달 (Dialog)
- **문제 해결**: 사용자가 매치 상세 정보에서 전체 10명의 데이터를 일일이 확인하며 자신의 라인 상대(Top vs Top, Mid vs Mid)를 찾고, 골드/딜량 차이를 머릿속으로 계산해야 하는 불편함 해소.
- **중요성**: LoL 플레이어에게 가장 직관적인 피드백은 "내가 라인전에서 이겼는가?"임. 이를 시각적으로 즉시 보여주어 인사이트의 깊이를 더함.

### 2. 최근 20게임 퍼포먼스 추세 그래프 (Trend Graph)
- **적용 위치**: `SummonerDetail` 페이지 상단 (레이더 차트 옆 혹은 아래)
- **문제 해결**: 현재 리스트 형태의 매치 기록으로는 나의 실력이 상승세인지 하락세인지, 혹은 최근 KDA가 좋아지고 있는지 한눈에 파악하기 어려움.
- **중요성**: 단순 스냅샷 점수가 아닌 '변화'를 보여줌으로써, 사용자에게 지속적인 방문 동기를 부여하고 시각적 만족도를 높임.

### 3. AI 분석 페르소나 선택 (Persona Selector)
- **적용 위치**: `SummonerDetail` > AI Analysis 섹션 상단
- **문제 해결**: 항상 동일한 톤앤매너의 AI 분석은 반복 사용 시 흥미가 떨어짐. 사용자 기분에 따라 "엄격한 코치", "부드러운 조언자", "팩트 폭격기" 등을 선택하고 싶음.
- **중요성**: 기술적 복잡도(프롬프트 엔지니어링) 대비 사용자 경험(재미 요소) 증대 효과가 큼. 포트폴리오 관점에서도 LLM 활용 능력을 보여주기 좋음.

### 4. 챔피언별 승률/숙련도 배지 (Mastery Badge)
- **적용 위치**: `SummonerDetail` > Recent Matches 리스트 아이템
- **문제 해결**: 매치 리스트에서 내가 잘하는 챔피언을 잡았을 때의 성적과, 연습 중인 챔피언의 성적을 구분해서 인식하기 어려움. "승률 60% 이상 챔피언" 등에 배지를 달아줌.
- **중요성**: 사용자의 자신감을 고취시키고, "이 챔피언은 나랑 잘 맞네"라는 긍정적 강화를 제공.

### 5. Mock AI 응답 동적화 (Dynamic Mock)
- **적용 위치**: `backend/core_api/ai_module.py` (MockAIProvider)
- **문제 해결**: API Key가 없는 데모 환경에서 Mock AI가 항상 똑같은 텍스트만 출력하여, 실제 데이터가 반영되지 않는다는 느낌을 줌.
- **중요성**: 실제 LLM 연동 없이도 입력된 `role_stats`의 최고/최저 점수를 기반으로 문장을 조합하면, 비용 없이 훨씬 그럴듯한 데모 경험을 제공할 수 있음.

---

## 2. Triage

### Top 1 Feature: 매치 상세 - 라인 상대 비교 (Head-to-Head)

**선정 이유**:
1.  **High UX Value**: LoL 분석의 핵심인 "상대와의 격차"를 가장 직관적으로 보여주는 기능입니다. 현재 테이블 형태의 데이터는 정보 과부하가 심하므로, 이를 요약해주는 비교 카드가 필수적입니다.
2.  **Feasibility**: 백엔드 변경 없이 프론트엔드(`MatchDetail` 모달)에서 이미 받은 데이터를 가공하여 구현할 수 있어 리스크가 낮습니다.
3.  **Portfoilo Impact**: 데이터를 단순히 나열하는 것이 아니라, 사용자가 원하는 형태로 '가공'하여 보여주는 UX 감각을 어필할 수 있습니다.

**탈락된 아이디어들**:
- *추세 그래프*: 구현 공수가 상대적으로 크고(`Recharts` 설정 등), 현재 MVP 단계에서는 개별 매치의 디테일을 보여주는 것이 우선이라 판단됨.
- *AI 페르소나*: 재미 요소이나, 핵심 분석 기능의 깊이를 더하는 것보단 우선순위가 낮음.
- *Mock AI 동적화*: 사용자 눈에 띄는 UI 변화가 적음.
- *챔피언 배지*: 현재 매치 데이터 양(20게임)으로는 통계적 유의미함을 찾기 어려울 수 있음.

---

## 3. Spec Draft

### Feature Name: Match Detail Head-to-Head Comparison

### Problem Statement
매치 상세 화면(`MatchDetail`)에서 사용자는 자신의 라인 상대가 누구인지 찾기 위해 적 팀 테이블을 스캔해야 하며, 주요 지표(골드, 딜량, CS)의 차이를 직접 계산해야 합니다. 이는 직관적인 성과 확인을 방해합니다.

### MVP Scope
- **대상**: `SummonerDetail` 페이지 내 매치 상세 다이얼로그(Dialog).
- **기능**:
  - 상세 정보 최상단(팀 테이블 위)에 `Head-to-Head` 섹션 추가.
  - 내 소환사 정보와 동일한 `lane` 값을 가진 적 팀 소환사를 자동 매칭.
  - 매칭된 상대가 있을 경우, 좌우 대칭 카드로 주요 스탯 비교 표시.
  - **비교 지표**: KDA, Total Damage, Total Gold, CS, Vision Score.
  - **시각적 강조**: 각 지표별로 더 높은 쪽에 텍스트 색상(Green/Blue) 강조 혹은 화살표 아이콘 표시.
- **예외 처리**:
  - 칼바람 나락(ARAM) 등 라인 개념이 희미한 경우, 혹은 상대 라이너를 특정할 수 없는 경우(데이터 누락) 해당 섹션을 숨김.

### Optional Scope
- 상대와의 아이템 빌드 순서 비교 (Timeline 데이터 필요하므로 MVP 제외).
- 골드 차이 그래프 (MVP 제외).

### Acceptance Criteria
1. 사용자가 매치 리스트를 클릭하여 상세 모달을 열면, 상단에 'VS' 섹션이 표시되어야 한다.
2. 내 캐릭터가 'JUNGLE'이라면, 적 팀의 'JUNGLE' 플레이어가 상대편에 표시되어야 한다.
3. 골드, 딜량 등 수치가 더 높은 쪽이 시각적으로 구분되어야 한다(예: 굵은 글씨 또는 색상).
4. 라인 정보가 없는 매치(예: ARAM)에서는 해당 섹션이 렌더링되지 않아야 한다.

---

## 4. Backlog Draft

### Github Issue Title
[Daily][2026-01-02] Feature: 매치 상세 화면에 라인 상대 비교(Head-to-Head) 섹션 추가

### Tasks
- [ ] **Frontend**: `MatchDetailResponse` 타입 및 기존 데이터를 활용하여 상대 라이너 찾기 유틸리티 함수(`findOpponent`) 구현.
- [ ] **Frontend**: `HeadToHeadCard` 컴포넌트 구현 (좌측 나, 우측 적, 중앙 VS 및 스탯 비교).
- [ ] **Frontend**: `SummonerDetail.tsx`의 `DialogContent` 내부에 `HeadToHeadCard` 배치 및 조건부 렌더링 처리.
- [ ] **Frontend**: 비교 로직 테스트 (내 데이터가 승리팀/패배팀일 때 모두 정상 작동 확인).

---

## 5. Docs / Notes

### README Update Suggestion
- (기능 구현 후) **Features** 섹션에 "Smart Match Analysis: Automatically compares performance against direct lane opponents." 문구 추가.

### Questions for Next Cycle
1. Riot API의 `lane` 정보가 부정확할 때(예: 스왑), `individualPosition`이나 `teamPosition`을 어떻게 우선순위로 둘 것인가? (현재 데이터 필드 확인 필요)
2. 서포터의 경우 CS나 딜량보다는 '시야 점수'나 'CC기 점수'가 더 중요한데, 역할군별로 비교 지표를 다르게 보여줄 수 있을까?
3. 모바일 뷰포트에서 가로 배치된 비교 카드가 좁아질 텐데, 세로 적층형으로 변경할 반응형 디자인이 필요한가?
