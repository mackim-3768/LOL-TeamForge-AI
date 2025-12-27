# Daily Idea Log: 2025-W10-day2

## 1. Discovery (Ideas)

1. **매치 리스트 상세 정보 펼치기 (Frontend)**
   - **위치:** 소환사 상세 페이지 - 매치 히스토리 리스트
   - **문제:** 현재 리스트에서는 KDA와 승패 여부만 확인 가능하여, 구체적인 아이템 빌드나 딜량 등 핵심 정보를 보려면 별도 페이지로 이동해야 하거나 아예 볼 수 없음.
   - **가치:** 사용자가 페이지 이동 없이 **깊이 있는 정보(Insight Depth)**를 즉시 확인할 수 있어 UX가 대폭 개선됨.

2. **라인전 상대방 비교 분석 (Backend)**
   - **위치:** AI 분석 리포트 / 매치 상세
   - **문제:** 단순히 "내가 잘했다/못했다"를 넘어, 맞라인 상대와 비교했을 때의 성과(CS 차이, 솔로킬 여부 등)가 궁금함.
   - **가치:** 상대적인 실력 척도를 제공하여 분석의 **구체성**을 확보함.

3. **AI 분석 페르소나 변경 기능 (AI/Frontend)**
   - **위치:** 설정 또는 분석 결과 창
   - **문제:** AI의 분석 톤이 일률적임. 때로는 엄격한 피드백을, 때로는 칭찬을 원할 수 있음.
   - **가치:** "엄격한 코치", "친절한 서포터" 등 페르소나를 선택하게 하여 **사용자 재미(Engagement)**와 개인화 경험 제공.

4. **팀 빌더 채팅 로그 파싱 (Frontend/Utils)**
   - **위치:** 팀 빌더 (Team Builder) 입력 화면
   - **문제:** 5명의 소환사 이름을 일일이 입력하는 것은 번거로움. 로비 채팅("XXX님이 로비에 참가하셨습니다")을 복사해 넣으면 자동 입력되길 원함.
   - **가치:** 입력 장벽을 낮추어 핵심 기능인 팀 추천 시스템의 **접근성(Accessibility)** 향상.

5. **챔피언 숙련도 뱃지 시스템 (Frontend)**
   - **위치:** 소환사 프로필 헤더
   - **문제:** 해당 소환사의 주력 챔피언이 무엇인지 한눈에 파악하기 어려움.
   - **가치:** 시각적 요소를 통해 소환사의 정체성을 빠르게 파악하게 돕고 **포트폴리오 시각화** 요소로 활용.

## 2. Triage

- **Top 1 Feature:** **매치 리스트 상세 정보 펼치기 (Expandable Match Details)**
- **선정 이유 (Selection Reasoning):**
  - **UX Impact:** 전적 검색 서비스에서 가장 기본적이면서도 빈번하게 사용되는 기능입니다. 사용자의 탐색 비용을 획기적으로 줄여줍니다.
  - **Feasibility:** 데이터는 이미 확보되어 있을 가능성이 높으며(Riot API Match V5), 프론트엔드 컴포넌트 확장 작업 위주라 리스크가 적습니다.
- **미선정 이유:**
  - 라인전 상대 분석: Riot API에서 상대 라이너를 정확히 매칭하는 로직(Role/Lane 보정)이 까다로울 수 있음.
  - 페르소나 변경: 핵심 분석 기능이 고도화된 후 추가하는 것이 적절함(Nice-to-have).

## 3. Spec Draft (Top 1 only)

### Feature: 매치 리스트 상세 정보 펼치기 (Expandable Match Details)

**Problem Statement:**
사용자는 매치 리스트에서 승패와 KDA 외에 아이템 빌드, 룬, 총 딜량 등 구체적인 게임 내용을 확인하려면 불편함을 겪습니다.

**MVP Scope:**
1. 매치 리스트의 각 행(Row)을 클릭 가능하게 변경 (Accordion UI 적용).
2. 클릭 시 하단으로 영역이 확장되며 다음 정보 표시:
   - 최종 아이템 빌드 (아이콘 6개 + 장신구)
   - 핵심 룬 및 보조 룬
   - 챔피언 가한 피해량 (Total Damage Dealt to Champions)
   - 와드 설치/제거 수 (Vision Stats)

**Optional Scope:**
- 팀원 10명의 간략한 정보 리스트 표시.
- 골드 획득 그래프.

**Acceptance Criteria:**
- [ ] 매치 리스트의 아이템/KDA 영역을 클릭하면 상세 패널이 부드럽게 펼쳐져야 한다.
- [ ] 상세 패널 내에 아이템 아이콘이 올바르게 로딩되어야 한다(Data Dragon URL 사용).
- [ ] 딜량, 받은 피해량, 시야 점수 등 주요 지표가 수치로 표시되어야 한다.

## 4. Backlog Draft

### GitHub Issue Title
`[Daily][2025-W10-day2] Implement Expandable Match Detail View`

### Task Breakdown
1. **[Frontend]** `MatchListItem` 컴포넌트를 Accordion 형태로 리팩토링 (state 관리 추가).
2. **[Frontend]** `MatchDetailPanel` 컴포넌트 구현 (아이템, 룬, 스탯 UI).
3. **[Frontend]** Data Dragon CDN URL 유틸리티 함수 확인 및 적용 (아이템 이미지용).
4. **[Docs]** UI 변경 사항 스크린샷 캡처 및 PR 첨부.

## 5. Docs / Notes

### Suggested README Update
- `Screenshots` 섹션이 있다면 "Detailed Match Analysis View" 추가.

### Questions for Next Cycle
1. 매치 데이터(MatchDTO)에 현재 룬(Perks) 정보와 아이템 정보가 포함되어 있는가? (백엔드 모델 확인 필요)
2. 아이템 아이콘 툴팁(아이템 설명)까지 구현할 것인가? (MUI Tooltip 활용 가능성)
3. 모바일 화면에서 상세 정보가 너무 길어지지 않도록 레이아웃을 어떻게 구성할 것인가?
